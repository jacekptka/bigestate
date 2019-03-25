from bs4 import BeautifulSoup
import requests

r = requests.get("https://gratka.pl/nieruchomosci/mieszkania/krakow")
soup = BeautifulSoup(r.content)


#with open("https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-upgrading-packages.html") as fp:
#    soup = BeautifulSoup(fp)

#soup = BeautifulSoup("<html>data</html>", "html.parser")
type(soup)
print(soup)