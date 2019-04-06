import os
import time
from bs4 import BeautifulSoup
import requests

city = "krakow"
citypl = "Kraków"
url2parse = "https://gratka.pl/nieruchomosci/mieszkania/" + city + "?page=1"
#print(url2parse)
r = requests.get(url2parse)
soup = BeautifulSoup(r.content,"html.parser")

mydir = 'D:'
myfile = 'big_bunch_of_immos'
target = os.path.join(mydir, myfile)
f = open(target ,"w+")

# get pagination
def get_max_pages():
    get_max_pages.max_pages = soup.find("input", {"aria-label":"Numer strony wyników"})['max']

#get number of articles on page
def get_max_articles():
    get_max_articles.max_articles = len(soup.find_all('article'))

def crawl_for_articles():
    get_max_pages()
    get_max_articles()

    for page in range(1, int(get_max_pages.max_pages)):

        url2parse_current = "https://gratka.pl/nieruchomosci/mieszkania/" + city + "?page="+str(page)
        r = requests.get(url2parse_current)
        soup = BeautifulSoup(r.content, "html.parser")

        #time.sleep(5)

        for article in range (0, get_max_articles.max_articles):

            teaser_params = soup.find_all('ul', class_='teaser__params')[article]
            teaser_price = 'Cena: ' + str(soup.find(attrs={'class' : 'teaser__price'}).contents[0].strip())
            teaser_anchor = 'Tytuł: ' + soup.find('a', class_='teaser__anchor').contents[0].strip()
            #teaser_location = 'Miasto: ' + soup.find('h3', class_='teaser__location').contents[0].strip().strip(',').strip('\\n')
            teaser_region = 'Województwo: ' + soup.find('span', class_='teaser__region').contents[0]
            params_from_teaser = [li.text.strip() for li in teaser_params.find_all('li')]
            params_from_teaser.append(teaser_price)
            params_from_teaser.append(teaser_anchor)
            #params_from_teaser.append(teaser_location)
            params_from_teaser.append(teaser_region)

            f.write(str(params_from_teaser)+"\n")
            #print(teaser_params)

crawl_for_articles()

f.close()

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





