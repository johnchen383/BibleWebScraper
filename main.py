import requests
from bs4 import BeautifulSoup

book = input("What book? ")
chapter = input("What chapter? ")
translation = input("What translation? [ESV, NIV, HWP] ")

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
chapterNum = results.find("span", class_="chapternum")
chapterNum.decompose()

text=""

for v in verses:
    # print(v.text.strip()),
    text=text+v.text.strip()+" "

print(text)