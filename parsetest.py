from bs4 import BeautifulSoup
import requests

r = requests.get("https://gratka.pl/nieruchomosci/mieszkania/krakow?page=1")
soup = BeautifulSoup(r.content,"html.parser")


# get pagination
max_pages = soup.find("input", {"aria-label":"Numer strony wyników"})['max']
print(max_pages)

#check if primary market
foundPrimaryMarket = soup.find("span", {"class":"teaser__primaryMarket"})
isPrimaryMarket = 0
if foundPrimaryMarket:
    isPrimaryMarket += 1
else:
    isPrimaryMarket += 0

#get city district
title = soup.find("a", {"class":"teaser__anchor"})['title'].split(' ')
for i in [i for i,x in enumerate(title) if x == 'Kraków']:
    print(title[i+1].strip(','))





#print(soup)

#gotowy loop
#for request in range(1, int(max_pages)+1):
#    page = requests.get("https://gratka.pl/nieruchomosci/mieszkania/krakow?page="+max_pages)
    #get whutcha want here
    #store it in dynamoDB
#    print(request)



