from bs4 import BeautifulSoup
import requests
import pandas as pd
import unicodedata
city = "krakow"
citypl = "Kraków"
url2parse = "https://gratka.pl/nieruchomosci/mieszkania/" + city + "?page=1"
#print(url2parse)
r = requests.get(url2parse)
soup = BeautifulSoup(r.content,"html.parser")


def transform_articles_onpage():

    teaser_params = soup.find('ul', class_='teaser__params')
    teaser_price = 'Cena: ' + str(soup.find(attrs={'class' : 'teaser__price'}).contents[0].strip())
    teaser_anchor = 'Tytuł: ' + soup.find('a', class_='teaser__anchor').contents[0].strip()
    teaser_location = 'Miasto: ' + soup.find('h3', class_='teaser__location').contents[0].strip().strip(',')
    teaser_region = 'Województwo: ' + soup.find('span', class_='teaser__region').contents[0]
    #params_from_teaser = [li.text.strip() for li in teaser_params.find_all('li')]
    #params_from_teaser.append(teaser_price)
    #params_from_teaser.append(teaser_anchor)
    #params_from_teaser.append(teaser_location)
    #params_from_teaser.append(teaser_region)

    #print(params_from_teaser)
    print(teaser_params)





transform_articles_onpage()

#            inner_ul = soup.find('ul', class_='innerUl')
 #           inner_items = [li.text.strip() for li in inner_ul.ul.find_all('li')]
#
 #           outer_ul_text = soup.ul.span.text.strip()
  #          inner_ul_text = inner_ul.span.text.strip()
#
   #         result = {outer_ul_text: {inner_ul_text: inner_items}}
    #        print result


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



