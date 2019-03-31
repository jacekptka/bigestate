from bs4 import BeautifulSoup
import requests
import unicodedata
city = "krakow"
citypl = "Kraków"
url2parse = "https://gratka.pl/nieruchomosci/mieszkania/" + city + "?page=1"
#print(url2parse)
r = requests.get(url2parse)
soup = BeautifulSoup(r.content,"html.parser")

articles = soup.find_all('article')

print(type(articles))
print(type(soup))

# get pagination
def get_max_pages():
    max_pages = soup.find("input", {"aria-label":"Numer strony wyników"})['max']
    return max_pages

# get_immo_number_onpage
def count_immos_onpage():
    count = 0
    articletags = soup.find_all('article')
    for tag in articletags:
        count += 1
    return count


#check if primary market
def check_if_primo():
    foundPrimaryMarket = articles.find("span", {"class":"teaser__primaryMarket"})
    isPrimaryMarket = 0
    if foundPrimaryMarket:
        isPrimaryMarket += 1
    else:
        isPrimaryMarket += 0
    return isPrimaryMarket

#get city district
def get_district():
    title = soup.find("a", {"class":"teaser__anchor"})['title'].split(' ')
    for i in [i for i,x in enumerate(title) if x == citypl]:
        return title[i+1].strip(',')


#print(get_max_pages())
#print(get_district())
#print(count_immos_onpage())
#print(check_if_primo())
#print(all_immos_on_page())

#gotowy loop
#for request in range(1, int(max_pages)+1):
#    page = requests.get("https://gratka.pl/nieruchomosci/mieszkania/krakow?page="+max_pages)
    #get whutcha want here
    #store it in dynamoDB
#    print(request)



