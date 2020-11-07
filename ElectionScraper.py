import requests
from bs4 import BeautifulSoup
import pandas as pd


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
            dataframe = pd.read_html(table)
            print(dataframe)

def getUCSBData(year):
    stateLst =  ["alaska", "alabama", "arkansas", "arizona", "california", "colorado", "connecticut", "dist. of col.", "delaware", "florida", "georgia", "hawaii", "iowa", "idaho", "illinois", "indiana", "kansas", "kentucky", "louisiana", "massachusetts", "maryland", "maine", "michigan", "minnesota", "missouri", "mississippi", "montana", "north carolina", "north dakota", "nebraska", "new hampshire", "new jersey", "new mexico", "nevada", "new york", "ohio", "oklahoma", "oregon", "pennsylvania", "rhode island", "south carolina", "south dakota", "tennessee", "texas", "utah", "virginia", "vermont", "washington", "wisconsin", "west Virginia", "wyoming"]
    r = requests.get("https://www.presidency.ucsb.edu/statistics/elections/" + str(year))
    soup = BeautifulSoup(r.content, "html.parser")
    table = soup.find("table",class_ = 'table table-responsive')
    df = pd.read_html(str(table))
    #I'm sure there's a better way to do it without using a python list, but pandas dfs are hard to learn
    entryLst = df[0].values.tolist()
    for entry in entryLst:
        #skips all entrys that aren't a state, just gotta parse it for candidate data now
        if str(entry[0]).lower() in stateLst:
            print(entry)

getUCSBData(1824)
