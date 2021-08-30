import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
# from fontTools.ttLib import TTFont
# font = TTFont('Helvetica.ttf')

book = input("What book? ")
chapter = input("Enter range. E.g. '1:1-2:4' OR '1' OR '2-3 ' ")
translation = input("What translation? [ESV, NIV, CSB, ASV, HWP] ")

URL = "https://www.biblegateway.com/passage/?search=" + book + "+" + chapter + "&version=" + translation + "&interface=print"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find("div", class_="text-html")
verses = results.find_all("span", class_="text")

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

# Formatting 'Selah', psalms, proverbs, psalm 119, psalms heading, song of songs headings, OT passage in NT,

for v in verses:
    text=text+v.text+" "



print(text)

#Create PDF
pdf = FPDF(orientation = 'P', unit = 'mm', format = 'A4')
pdf.set_margins(30, 20, 30)
pdf.add_page()
pdf.add_font('Helvetica', '', 'Helvetica.ttf', uni=True)
pdf.set_font('Helvetica', style = '', size = 12)
pdf.set_text_color(0, 0, 0)

pdf.write(10, text)

#Output
pdf.output('Manuscript.pdf')