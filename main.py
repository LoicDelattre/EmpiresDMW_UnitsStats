import requests
from bs4 import BeautifulSoup
import csv

homePageUrl = "https://empireearth.fandom.com/wiki/Category:Empires:_Dawn_of_the_Modern_World_Units"
baseUrl = "https://empireearth.fandom.com"

pageHome = requests.get(homePageUrl, verify = False)

htmlDataHome = BeautifulSoup(pageHome.content, "html.parser")
unitsSpace = htmlDataHome.find_all("div", class_ = "category-page__member-left")


unitsLinks = []

unitsOutputData = []


for item in unitsSpace:
    attribute = item.find_all("a")[0] #outpus a 1 element list hence [0]
    linkUnit = baseUrl + attribute["href"]

    pageUnit = requests.get(linkUnit, verify = False)
    htmlDataUnit = BeautifulSoup(pageUnit.content, "html.parser")
    unitData = htmlDataUnit.find_all("div", class_ = "mw-parser-output")[0]

    ###LEFT HTML###
    #get summary
    summarySpace = unitData.find_all("p")[1]
    summary = summarySpace.get_text().replace("in Empires: Dawn of the Modern World.\n", "")

    #get strength and weaknesses
    subtitleSpaces = unitData.find_all("h2")
    firstSubTitle = subtitleSpaces[5].get_text().replace("[", "").replace("]", "")
    SubSpace = unitData.find_all("ul")
    firstSub = SubSpace[0].get_text()

    if firstSubTitle == "Strengths":
        strength = firstSub
        weakness = SubSpace[1].get_text()
    
    elif firstSubTitle == "Weaknesses": 
        strength = "None"
        weakness = firstSub
    
    ###RIGHT HTML###
    dataAreas = unitData.find_all("section")

    #unit info
    infoAreas = dataAreas[0].find_all("div", class_ = "pi-item pi-data pi-item-spacing pi-border-color")
    era = infoAreas[1].find("a").get_text()
    nation = infoAreas[2].find("a").get_text()
    building = infoAreas[3].find("span").get_text()
    typeList = infoAreas[4].get_text().split()
    type = ' '.join(typeList).replace("Type ", "")

    #unit stats
    statsAreas = dataAreas[1].find_all("div", class_ = "pi-item pi-data pi-item-spacing pi-border-color")
    stats = {}
    for i in range(len(statsAreas)):
        stats[statsAreas[i].find("h3").get_text()] = statsAreas[i].find("div").get_text()
    
    #production stats
    productionAreas = dataAreas[2].find_all("div", class_ = "pi-item pi-data pi-item-spacing pi-border-color")
    costList = productionAreas[1].find("div").get_text().split()
    cost = {}
    for i in range(int(len(costList)/2)):
        cost[costList[2*i+1]] = costList[2*i]
    pop_count = productionAreas[2].find("div").get_text().replace(" ", "")
    
    unitOut = {
        "SUMMARY": summary,
        "STRENGTHS": strength, 
        "WEAKNESSES": weakness,
        "ERA": era,
        "NATION": nation,
        "BUILDING": building,
        "TYPE": type,
        "STATS": stats,
        "COST": cost,
        "POP COUNT": pop_count
    }   

    unitsOutputData.append(unitOut)
    print(unitOut)

with open("UnitsRawData.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(unitsOutputData[0].keys())
    for i in range(len(unitsOutputData)):
        writer.writerow(unitsOutputData[i].values())

