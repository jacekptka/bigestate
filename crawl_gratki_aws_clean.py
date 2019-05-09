import random
import string
import re

import boto3
import os
import time
from bs4 import BeautifulSoup
import requests

city = "krakow"
citypl = "Kraków"
url2parse = "https://gratka.pl/nieruchomosci/mieszkania/" + city + "?page=1"

r = requests.get(url2parse)
soup = BeautifulSoup(r.content,"html.parser")

session = boto3.Session(profile_name='default')
s3_bucket_name = "jpi-bigestate"

s3 = session.resource('s3')
s3_bucket = s3.Bucket(s3_bucket_name)

# get number of pages
def get_max_pages():
    get_max_pages.max_pages = soup.find("input", {"aria-label":"Numer strony wyników"})['max']

# get number of articles on page
def get_max_articles():
    get_max_articles.max_articles = len(soup.find_all('article'))

def crawl_for_articles():
    get_max_pages()
    get_max_articles()
    crawl_for_articles.estates = ""
    crawl_for_articles.header = ""

    for page in range(1, int(get_max_pages.max_pages)):


        url2parse_current = "https://gratka.pl/nieruchomosci/mieszkania/" + city + "/sprzedaz?page="+str(page)
        r = requests.get(url2parse_current)
        soup = BeautifulSoup(r.content, "html.parser")

        for article in range (0, get_max_articles.max_articles):

            # Get features: area, number of rooms, floor
            teaser_params = soup.find_all('ul', class_='teaser__params')[article]
            teaser_price = 'price:' + soup.find_all('p', class_='teaser__price')[article].contents[0].strip().replace(" ","")
            teaser_anchor = 'title:' + soup.find_all('a', class_='teaser__anchor')[article].contents[0].strip().replace(",","")
            striped_teaser_params = [li.text.strip() for li in teaser_params.find_all('li')]
            if striped_teaser_params[0].startswith("O"):
                params_from_teaser = striped_teaser_params[1:4]
            else:
                params_from_teaser = striped_teaser_params[:3]

            params_from_teaser = [w.replace('Powierzchnia w m2', 'area') for w in params_from_teaser]
            params_from_teaser = [w.replace('Liczba pokoi', 'no_of_rooms') for w in params_from_teaser]
            params_from_teaser = [w.replace('Piętro', 'level') for w in params_from_teaser]
            params_from_teaser = [w.replace('parter', '0') for w in params_from_teaser]
            params_from_teaser = [re.sub(r'piwnica(.*)', '-1', w) for w in params_from_teaser]

            params_from_teaser.append(teaser_price)
            params_from_teaser.append(teaser_anchor)

            # Check if it's primary ir secondary market
            foundPrimaryMarket = soup.find_all("span", {"class": "teaser__primaryMarket"})
            isPrimaryMarket = ""
            if foundPrimaryMarket:
                isPrimaryMarket += "yes"
            else:
                isPrimaryMarket += "no"

            params_from_teaser.append("primary_market:"+isPrimaryMarket)

            # What district?
            district = ""
            title = teaser_anchor.split(' ')
            for i in [i for i, x in enumerate(title) if x == citypl]:
                try:
                    district = title[i + 1]
                    if district == 'Stare':
                        district = "Stare Miasto"
                    if district == 'Nowa':
                        district = "Nowa Huta"
                    if district == 'Wola':
                        district = "Wola Justowska"
                except IndexError:
                    district = "brak"

            params_from_teaser.append("district:" + str(district.strip(',')))

            # Formatting data CSV-like
            keys = []
            values =[]
            for i in params_from_teaser:
                ention = i.split(":")
                keys.append(ention[0])
                values.append(ention[1])

            crawl_for_articles.header = str(keys).replace("'","").replace("[","").replace("]","").replace(" ", "")+'\n'
            estate = str(values)
            temp = estate.replace("'","").replace("[","").replace("]","")
            crawl_for_articles.estates += temp+'\n'
            print(str(page)+str(article))


# Execute main function and write to S3
crawl_for_articles()

body = crawl_for_articles.header + crawl_for_articles.estates
object_name = 'estates_' + city + time.strftime("%Y%m%d-%H%M%S") + '.txt'
s3.Bucket(s3_bucket_name).put_object(Key=object_name, Body=body, ContentType='text/plain')






