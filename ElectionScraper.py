import requests
from bs4 import BeautifulSoup
import pandas as pd
import math

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

    stateList = {"alaska": None, "alabama": None, "arkansas": None, "arizona": None, "california": None, "colorado": None,
                 "connecticut": None, "dist. of col.": None, "delaware": None, "florida": None, "georgia": None, "hawaii": None,
                 "iowa": None, "idaho": None, "illinois": None, "indiana": None, "kansas": None, "kentucky": None, "louisiana": None,
                 "massachusetts": None, "maryland": None, "maine": None, "michigan": None, "minnesota": None, "missouri": None,
                 "mississippi": None, "montana": None, "north carolina": None, "north dakota": None, "nebraska": None,
                 "new hampshire": None, "new jersey": None, "new mexico": None, "nevada": None, "new york": None, "ohio": None,
                 "oklahoma": None, "oregon": None, "pennsylvania": None, "rhode island": None, "south carolina": None,
                 "south dakota": None, "tennessee": None, "texas": None, "utah": None, "virginia": None, "vermont": None,
                 "washington": None, "wisconsin": None, "west Virginia": None, "wyoming": None}


    df = pd.read_html("https://www.presidency.ucsb.edu/statistics/elections/" + str(year))
    # I'm sure there's a better way to do it without using a python list, but pandas dfs are hard to learn
    # you think he'll be upset that pandas is doing some of the scraping work?
    # ^^ Who cares?
    entryLst = df[0].values.tolist()
    header = []
    candidates = []
    allCandidateData = []
    for entry in entryLst:
        # skips all entry's that aren't a state, just gotta parse it for candidate data now
        if str(entry[0]).lower() in stateList:
            stateList[str(entry[0]).lower()] = entry[2:]

        elif str(entry[0]).lower() == "state":  # need to extract the header
            header.append(entry[2:])

    x = 0
    while x < len(header[0]):  # builds a list of candidates and their party
        candidates.append([header[1][x], header[0][x]])
        x += 3  # replicates each item 3X
    print(candidates)
    infile = open("test_results.txt","w")
    for state in stateList:
        newData = []
        if stateList[state] is not None:
            y = 0
            newData = []
            for candidate in candidates:
                newData += candidate
                candidateData = []
                while True:
                    newData.append(stateList[state][y])
                    candidateData.append(stateList[state][y])
                    y += 1
                    if y % 3 == 0:
                        break
                candidateLst = [year, state, candidate[0], candidate[1], candidateData[0]]
                candidateStr = str(year)+','+state+','+candidate[0]+','+candidate[1]+','+candidateData[0]
                #If the candidate recieved no electoral votes from the state

                if type(candidateData[2]) == float and math.isnan(candidateData[2]):
                    candidateLst.append("0")
                    candidateStr += ",0"
                else:
                    candidateLst.append(candidateData[2])
                    candidateStr += ","+candidateData[2]
                allCandidateData.append(candidateLst)
                print(candidateStr, file=infile)

        if newData:
            print(state, end=" ")
            print(newData)  # this needs to get cleaned up but holds the right data.
            print(allCandidateData)
    infile.close()
    print("titty")





getUCSBData(1824)
