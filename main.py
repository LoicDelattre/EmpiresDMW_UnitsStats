import requests


homePageUrl = "https://empireearth.fandom.com/wiki/Category:Empires:_Dawn_of_the_Modern_World_Units"

page = requests.get(homePageUrl, verify = False)

print(page.text)

