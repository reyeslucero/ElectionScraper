import requests
from bs4 import BeautifulSoup
import pandas as pd
import math

START_DATE = 1824
END_DATE = 2016


# def getData(year):
#     r = requests.get("https://en.wikipedia.org/wiki/" + str(year) + "_United_States_presidential_election")
#     soup = BeautifulSoup(r.content, "html.parser")
#     tables = soup.findAll("table")
#     stateResults = tables[20]
#     links = []
#     for link in stateResults.find_all('a'):
#         links.append(link.get('href'))
#     for link in links:
#         parseStateTable(link)


# def parseStateTable(link):
#     if link is not None and link[:6] == "/wiki/":
#         r = requests.get("https://en.wikipedia.org" + link)
#         soup = BeautifulSoup(r.content, "html.parser")
#         header = soup.find("span", {"id": "Results"})
#         if header is not None:  # now we're in the real meat and potatoes of this
#             table = header.find_next("table")
#             print(table)  # prolly pandas is the next move for this
#             dataFrame = pd.read_html(table)
#             print(dataFrame)
#

def getUCSBData(year, infile):

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
    startIndex = 2
    minorCandidates = []

    row = entryLst[startIndex]

    emptyRow = False
    while not emptyRow:

        name = row[3]
        electoral = row[5]
        popular = row[8]

        startIndex += 1
        row = entryLst[startIndex]
        emptyRow = (type(row[1]) == float) and math.isnan(row[1])

        if electoral == '0':
            minorCandidates.append(name.upper())

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
        candidate = header[1][x]
        party = header[0][x]
        if type(candidate) == float and math.isnan(candidate):
            break
        candidates.append([candidate, party])
        x += 3  # replicates each item 3X
    print(str(year) + ": " + str(candidates))

    for state in stateList:
        if stateList[state] is not None:
            y = 0
            for candidate in candidates:
                candidateData = []
                while True:
                    # newData.append(stateList[state][y])
                    if type(stateList[state][y]) == float and math.isnan(stateList[state][y]):
                        candidateData.append("0")
                    else:
                        candidateData.append(stateList[state][y])
                    y += 1
                    if y % 3 == 0:
                        break
                if candidate[0] not in minorCandidates:
                    candidateStr = str(year)+','+state+','+candidate[0]+','+candidate[1]+','+candidateData[0]
                    candidateStr += ","+candidateData[2]
                    print(candidateStr, file=infile)
                else:
                    print(candidate[0])



if __name__ == "__main__":
    cur = START_DATE
    infile = open("ElectionResults.txt", "w")
    while cur <= END_DATE:
        getUCSBData(cur, infile)
        cur += 4
    infile.close()

