import random
import string

import boto3
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



session = boto3.Session(profile_name='default')
#s3_content_type = os.environ.get('S3_CONTENT_TYPE', 'text/plain')
s3_bucket_name = "jpi-bigestate"

s3 = session.resource('s3')
s3_bucket = s3.Bucket(s3_bucket_name)


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

        url2parse_current = "https://gratka.pl/nieruchomosci/mieszkania/" + city + "/sprzedaz?page="+str(page)
        r = requests.get(url2parse_current)
        soup = BeautifulSoup(r.content, "html.parser")

        for article in range (0, get_max_articles.max_articles):

            teaser_params = soup.find_all('ul', class_='teaser__params')[article]
            teaser_price = 'Cena: ' + soup.find_all('p', class_='teaser__price')[article].contents[0].strip().replace(" ","")
            teaser_anchor = 'Tytuł: ' + soup.find_all('a', class_='teaser__anchor')[article].contents[0].strip().replace(",","")
            #teaser_location = 'Miasto: ' + soup.find('h3', class_='teaser__location').contents[0].strip().strip(',').strip('\\n')
            #teaser_region = 'Województwo: ' + soup.find('span', class_='teaser__region').contents[0]
            striped_teaser_params = [li.text.strip() for li in teaser_params.find_all('li')]
            if striped_teaser_params[0].startswith("O"):
                params_from_teaser = striped_teaser_params[1:4]
            else:
                params_from_teaser = striped_teaser_params[:3]

            params_from_teaser.append(teaser_price)
            params_from_teaser.append(teaser_anchor)
            #params_from_teaser.append(teaser_location)
            #params_from_teaser.append(teaser_region)

            #sprawdź czy rynek pierwotny
            foundPrimaryMarket = soup.find("span", {"class": "teaser__primaryMarket"})
            isPrimaryMarket = ""
            if foundPrimaryMarket:
                isPrimaryMarket += "tak"
            else:
                isPrimaryMarket += "nie"

            params_from_teaser.append("Rynek Pierwotny: "+isPrimaryMarket)

            #dzielnica
            district = ""
            title = soup.find("a", {"class": "teaser__anchor"})['title'].split(' ')
            for i in [i for i, x in enumerate(title) if x == citypl]:
                if title.index(citypl)+1 < len(title):
                    district = title[i + 1]
                    if district == 'Stare':
                        district = "Stare Miasto"
                    if district == 'Nowa':
                        district = "Nowa Huta"
                else:
                    district = "brak"
                #if title[i + 1] != 0:
                 #   district = title[i + 1].strip(',')
                #else:
                 #   district = "brak"

            params_from_teaser.append("Dzielnica: " + str(district.strip(',')))

            keys = []
            values =[]
            for i in params_from_teaser:

                ention = i.split(":")
                keys.append(ention[0])
                values.append(ention[1])

            estate = str(keys)+'\n'+str(values)
            body = estate.replace("'","").replace("[","").replace("]","")

            #print(body)

            object_name = 'estates_'+city+'_'+str(page)+'_'+str(article)+'.json'
            s3.Bucket(s3_bucket_name).put_object(Key=object_name, Body=body, ContentType='text/plain')


crawl_for_articles()



#f.close()


#get city district
def get_district():
    title = soup.find("a", {"class":"teaser__anchor"})['title'].split(' ')
    for i in [i for i,x in enumerate(title) if x == citypl]:
        return title[i+1].strip(',')







