import requests
from bs4 import BeautifulSoup

homePageUrl = "https://empireearth.fandom.com/wiki/Category:Empires:_Dawn_of_the_Modern_World_Units"
baseUrl = "https://empireearth.fandom.com/"

page = requests.get(homePageUrl, verify = False)

htmlData = BeautifulSoup(page.content, "html.parser")

unitsSpace = htmlData.find_all("div", class_ = "category-page__member-left")

unitsLinks = []

for item in unitsSpace:
    attribute = item.find_all("a")[0] #outpus a 1 element list hence [0]
    unitsLinks.append(attribute["href"])

<<<<<<< HEAD
print(unitsLinks)
=======
print(unitsLinks)
>>>>>>> develop
