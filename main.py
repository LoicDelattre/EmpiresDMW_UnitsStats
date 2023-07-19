import requests
from bs4 import BeautifulSoup
import csv
import time

start_time = time.time()

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
    unitName = attribute["href"].split("/")[2]

    pageUnit = requests.get(linkUnit, verify = False)
    htmlDataUnit = BeautifulSoup(pageUnit.content, "html.parser")
    for i in range(len(htmlDataUnit.find_all("div", class_ = "mw-parser-output"))):
        checkData = htmlDataUnit.find_all("div", class_ = "mw-parser-output")[i]
        if len(checkData) >20:
            unitData = checkData

    ###LEFT HTML###
    #get summary
    summarySpace = unitData.find_all("p")[1]
    if len(unitData.find_all("p")) > 2:
        summarySpace = unitData.find_all("p")[len(unitData.find_all("p"))-1]
    summary = summarySpace.get_text().replace("in Empires: Dawn of the Modern World", "").replace("\n", "")

    #get strength and weaknesses
    strength = "None"
    weakness = "None"
    weakCheck = False
    strengthCheck = False
    
    for ul in unitData.find_all("ul"):
        if "Strengths" in ul.find_previous("h2").get_text() and strengthCheck == False:
            strength = ul.get_text()
            strengthCheck = True
    
        elif "Weaknesses" in ul.find_previous("h2").get_text() and weakCheck == False: 
            weakness = ul.get_text()
            weakCheck = True
    
    
    ###RIGHT HTML###
    dataAreas = unitData.find_all("section")

    #unit info
    infoAreas = dataAreas[0].find_all("div", class_ = "pi-item pi-data pi-item-spacing pi-border-color")
    categRecord = []
    nationCount = 0
    type = "None"
    for i in range(len(infoAreas)):
        category = infoAreas[i]["data-source"]
        categRecord.append(category)
        if category == "Epoch":
            try:
                era = infoAreas[i].find("a").get_text()
            except:
               era = infoAreas[i].find("div").get_text() #if the era has a link
        elif category == "Trained At":
            try:
                building = infoAreas[i].find("span").get_text()
            except:
                building = infoAreas[i].find("a").get_text() #if the building has a link
        elif category == "Type":
            typeList = infoAreas[i].get_text().split()
            type = ' '.join(typeList).replace("Type ", "")
        elif category == "Civilization":
            nation = infoAreas[i].find("a").get_text()
            nationCount += 1

    typeList = ["Anti-Tank", "Anti-Air"]
    typeDetection = ["(AT)", "(AA)"]

    if len(type.split("/")) > 1:
        typeID = []
        for i in range(len(type.split("/"))):
            typeIndex = typeList.index(type.split("/")[i])
            typeID.append(typeDetection[typeIndex])

    countries = ["France", "United Kingdom", "United States", "Russia", "Korea", "China", "Germany"]
    nationList = []
    nationIndexes = []
    if "Civilization" not in categRecord:
        nationalities = ["French", "English", "American", "Russian", "Korean", "Chinese", "German"]
        for i in range(len(nationalities)):
            if nationalities[i] in summary.split():
                if nationalities[i] == "Germans":
                    nationList.append("Germany")
                else:
                    nationList.append(countries[i])
                nationIndexes.append(i)
                nationCount += 1
    else:
        nationList.append(nation)
    statNation = ["(France)", "(UK)", "(USA)", "(Russia)", "(Korea)", "(China)"]
    for nationItr in range(nationCount):
        nation = nationList[nationItr]

        #unit stats
        statsAreas = dataAreas[1].find_all("div", class_ = "pi-item pi-data pi-item-spacing pi-border-color")
        stats = {}
        for i in range(len(statsAreas)):
            statList = statsAreas[i].find("div").get_text().split()
            if len(statList) > 1 and nationCount > 1:
                statID = statNation[nationIndexes[nationItr]]
                middle = statList[1].split(")")
                statList[1] = middle[0] + ")"
                statList.insert(2, middle[1])
                if '' in statList:
                    statList.remove('')
                if statID not in statList:
                    stats[statsAreas[i].find("h3").get_text()] = "0"
                else:
                    statIndex = statList.index(statID)
                    stats[statsAreas[i].find("h3").get_text()] = statList[statIndex -1]

            elif len(statList) > 1 and nationCount <= 1:
                if len(statList[1].replace("(", "").split()) > 1:
                    middle = statList[1].split(")")
                    statList[1] = middle[0] + ")"
                    statList.insert(2, middle[1])
                    if '' in statList:
                        statList.remove('')
                    for j in range(len(typeID)):
                        if typeID[j] in statList:
                            stats[statsAreas[i].find("h3").get_text() + " " + typeID[j]] = statList[statList.index(typeID[j])-1]
                elif len(statList[1].replace("(", "").split()) == 1:
                    if len(statList) == 5:
                        typeID = ["", "Bombardment Mode"]
                        statList = [statList[0], statList[1].replace("(", "")]
                        for j in range(len(typeID)):
                            if typeID[j] in statList:
                                stats[statsAreas[i].find("h3").get_text() + " " + typeID[j]] = statList[j]
                    elif len(statList) == 4:
                        typeID = ["", "in Cannonade"]
                        statList = [statList[0], statList[1].replace("(", "")]
                        for j in range(len(typeID)):
                            if typeID[j] in statList:
                                stats[statsAreas[i].find("h3").get_text() + " " + typeID[j]] = statList[j]
            else:
                stats[statsAreas[i].find("h3").get_text()] = statsAreas[i].find("div").get_text().replace(" ", "")
    
        #production stats
        productionAreas = dataAreas[2].find_all("div", class_ = "pi-item pi-data pi-item-spacing pi-border-color")
        abilities = "None"
        cost = "None"
        buildingRequired = "None"
        pop_count = "None"
        for i in range(len(productionAreas)):
            category = productionAreas[i]["data-source"]
            if category == "Cost":
                costList = productionAreas[i].find("div").get_text().split()
                if ',' in costList:
                    costList.remove(',')
                cost = {}
                for j in range(int(len(costList)/2)):
                    cost[costList[2*j+1]] = costList[2*j].replace(" ", "")
            elif category == "Pop Count":
                pop_count = productionAreas[i].find("div").get_text().replace(" ", "")
            elif category == "Requires":
                buildingRequired = productionAreas[i].find("div").get_text().replace(" ", "")  
            elif category == "Abilities":
                abilities =  productionAreas[i].find("div").get_text().split()   
        unitOut = {
            "UNIT": unitName,
            "SUMMARY": summary,
            "STRENGTHS": strength, 
            "WEAKNESSES": weakness,
            "ERA": era,
            "NATION": nation,
            "BUILDING": building,
            "TYPE": type,
            "STATS": stats,
            "BUILDING REQUIRED": buildingRequired,
            "ABILITIES": abilities,
            "COST": cost,
            "POP COUNT": pop_count
        }   

        unitsOutputData.append(unitOut)
        #print(unitOut)

print("Run Time: %s seconds" % (time.time() - start_time))

with open("UnitsRawData.csv", "w", newline = "") as f:
    writer = csv.writer(f)
    writer.writerow(unitsOutputData[0].keys())
    for i in range(len(unitsOutputData)):
        writer.writerow(unitsOutputData[i].values())

