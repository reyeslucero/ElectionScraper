import requests
from bs4 import BeautifulSoup
import pandas as pd
import math

START_DATE = 1824
END_DATE = 2016


def getUCSBData(year, infile, unpopularFile):

    stateList = {"alaska": None, "alabama": None, "arkansas": None, "arizona": None, "california": None,
                 "colorado": None, "connecticut": None, "dist. of col.": None, "delaware": None, "florida": None,
                 "georgia": None, "hawaii": None, "iowa": None, "idaho": None, "illinois": None, "indiana": None,
                 "kansas": None, "kentucky": None, "louisiana": None, "massachusetts": None, "maryland": None,
                 "maine": None, "michigan": None, "minnesota": None, "missouri": None, "mississippi": None,
                 "montana": None, "north carolina": None, "north dakota": None, "nebraska": None, "new hampshire": None,
                 "new jersey": None, "new mexico": None, "nevada": None, "new york": None, "ohio": None,
                 "oklahoma": None, "oregon": None, "pennsylvania": None, "rhode island": None, "south carolina": None,
                 "south dakota": None, "tennessee": None, "texas": None, "utah": None, "virginia": None,
                 "vermont": None, "washington": None, "wisconsin": None, "west virginia": None, "wyoming": None}

    df = pd.read_html("https://www.presidency.ucsb.edu/statistics/elections/" + str(year))

    entryLst = df[0].values.tolist()
    startIndex = 3
    if year == 1976:
        startIndex = 2
    minorCandidates = []
    candidates = []
    majorCandidates = []

    row = entryLst[startIndex]

    emptyRow = False
    while not emptyRow:
        name = row[3]
        electoral = row[5]
        party = row[1]
        if year == 2016:
            if row[0][:4] == "Last":
                break
            party = row[0]
            name = row[2]
            electoral = row[4]

        if electoral == '0':
            minorCandidates.append(name.upper())
        if electoral != '0':
            minor = False
            for candidate in majorCandidates:
                if candidate[1] == party:  # dont include multiples from the same party
                    minor = True
            if not minor:
                majorCandidates.append([name.upper(), party])

        startIndex += 1
        if startIndex > (len(entryLst) - 1):
            break
        row = entryLst[startIndex]
        emptyRow = (type(row[1]) == float and math.isnan(row[1]))
        if year == 2016:
            emptyRow = (type(row[2]) == float and math.isnan(row[2]))

    if year == 1976:
        entryLst = df[1].values.tolist()
    header = []
    # for entry in entryLst:
    #     # skips all entry's that aren't a state, just gotta parse it for candidate data now
    #     if str(entry[0]).lower() in stateList:
    #         stateList[str(entry[0]).lower()] = entry[2:]
    #
    #     elif str(entry[0]).lower() == "state":  # need to extract the header
    #         header.append(entry[2:])
    for i in range(len(entryLst)):
        if str(entryLst[i][0]).lower() in stateList:
            stateList[str(entryLst[i][0]).lower()] = entryLst[i][2:]

        elif str(entryLst[i][0]).lower() == "state":  # need to extract the header
            # header.append(entryLst[i-1][2:])
            header.append(entryLst[i][2:])

    x = 0
    if year < 1900:
        while x < len(header[0]):  # builds a list of candidates and their party
            candidate = header[1][x]
            party = header[0][x]
            if type(candidate) == float and math.isnan(candidate):
                break
            if [candidate, party] not in candidates:
                candidates.append([candidate, party])
            x += 1  # replicates each item 3X

    else:
        candidates = majorCandidates

    for state in stateList:
        if stateList[state] is not None:
            y = 0
            for candidate in candidates:
                candidateData = []
                while True:
                    if type(stateList[state][y]) == float and math.isnan(stateList[state][y]):
                        candidateData.append("0")
                    else:
                        candidateData.append(stateList[state][y])
                    y += 1
                    if y % 3 == 0:
                        break
                if candidate[0] not in minorCandidates:
                    if candidateData[0] == "--":  # TODO verify that this is the right action in this circumstance
                        candidateData[0] = "0"
                    candidateStr = str(year)+','+state+','+candidate[0]+','+candidate[1]+','+candidateData[0]
                    candidateStr += ","+candidateData[2]
                    if "legislature" in candidateData[2]:
                        print(candidateStr, file=unpopularFile)
                    else:
                        print(candidateStr, file=infile)


def isNAN(num):
    return(type(num) == float) and math.isnan(num)


if __name__ == "__main__":
    cur = START_DATE
    infile = open("ElectionResults.txt", "w")
    unpopularFile = open("UnpopularElectoralVotes.txt","w")
    while cur <= END_DATE:
        try:
            getUCSBData(cur, infile,unpopularFile)
            print("Successfully scraped election of: " + str(cur))
        except:
            print("Error with election of: " + str(cur))
        cur += 4
    infile.close()
    unpopularFile.close()

