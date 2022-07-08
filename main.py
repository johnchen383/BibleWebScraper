import requests
from bs4 import BeautifulSoup
from fpdf import FPDF

book = input("What book? ")
chapter = input("Enter range. E.g. '1:1-2:4' OR '1' OR '2-3' ")
translation = input("What translation? [ESV, NIV, CSB, ASV, HWP] ")

header = book.title() + " " + chapter + " [" + translation.upper() + "]\n\n"

URL = "https://www.biblegateway.com/passage/?search=" + book + "+" + chapter + "&version=" + translation + "&interface=print"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find("div", class_="text-html")

#Get rid of subheadings
head = results.find_all("h3")
for h in head:    
    h.decompose()

# Get rid of verse numbers
sup = results.find_all("sup")
for s in sup:    
    s.decompose()

# Get rid of chapter numbers
chapterNum = results.find_all("span", class_="chapternum")
for c in chapterNum:
    c.decompose()

#Get smallcaps text
smallCaps = results.find_all("span", class_="small-caps")
for s in smallCaps:
    text=s.text.upper()
    s.replace_with(text)

text=""

paragraphs = soup.find_all(["p", "h4"])

for p in paragraphs:   
    verses = p.find_all("span", class_="text")
    
    if len(verses) == 0:
        continue

    for v in verses:
        text+=v.text+" "
        
        if p.get('class') == None:
            continue

        if "line" in p.get('class'):
            text+="\n"

    if p.get('class') == None:
        text+="\n\n"
        continue

    if "line" in p.get('class'):
        text+="\n"
    else:
        text+="\n\n"


#Format 'Selah'
if book.lower() == "psalm":
    text = text.replace("Selah", "        Selah")

text=text.replace("\u02BC", "'")

print(text)


#Create PDF
pdf = FPDF(orientation = 'P', unit = 'mm', format = 'A4')
pdf.set_margins(30, 20, 30)
pdf.add_page()
pdf.add_font('Helvetica', '', 'Helvetica.ttf', uni=True)
pdf.set_text_color(0, 0, 0)

pdf.set_font('Helvetica', style = '', size = 24)
pdf.write(7, header)

pdf.set_font('Helvetica', style = '', size = 12)

#Write line numbers
# spacing=7
# limit=34
# initx=22
# inity=32

# for i in range(1, limit + 1):
#     pdf.text(initx, inity + i * spacing, str(i))



pdf.write(7, text)

#Output
pdf.output('Manuscript.pdf')