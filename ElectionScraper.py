import requests
from bs4 import BeautifulSoup


START_DATE = 1824
END_DATE = 2016


def getData(year):
    r = requests.get("https://en.wikipedia.org/wiki/" + str(year) + "_United_States_presidential_election")
    soup = BeautifulSoup(r.content, "html.parser")
    tables = soup.findAll("table")
    stateResults = tables[20]
    links = []
    for link in stateResults.find_all('a'):
        links.append(link.get('href'))
    for link in links:
        parseStateTable(link)


def parseStateTable(link):
    if link is not None and link[:6] == "/wiki/":
        r = requests.get("https://en.wikipedia.org" + link)
        soup = BeautifulSoup(r.content, "html.parser")
        header = soup.find("span", {"id": "Results"})
        if header is not None:  # now we're in the real meat and potatoes of this
            table = header.find_next("table")
            print(table)  # prolly pandas is the next move for this


getData(1824)
