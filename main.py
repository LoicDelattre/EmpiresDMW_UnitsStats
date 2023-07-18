import requests
from bs4 import BeautifulSoup

homePageUrl = "https://empireearth.fandom.com/wiki/Category:Empires:_Dawn_of_the_Modern_World_Units"
baseUrl = "https://empireearth.fandom.com/"

pageHome = requests.get(homePageUrl, verify = False)

htmlDataHome = BeautifulSoup(pageHome.content, "html.parser")

unitsSpace = htmlDataHome.find_all("div", class_ = "category-page__member-left")

unitsLinks = []

for item in unitsSpace:
    attribute = item.find_all("a")[0] #outpus a 1 element list hence [0]
    linkUnit = baseUrl + attribute["href"]

    pageUnit = requests.get(linkUnit, verify = False)
    htmlDataUnit = BeautifulSoup(pageUnit.content, "html.parser")
    unitData = htmlDataUnit.find_all("div", class_ = "mw-parser-output")[0]
    print(unitData)

    break 
    for area in unitData:
        summary = area.find_all("p")
        print(area)
        break
    break