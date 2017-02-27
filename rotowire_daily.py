#-------------------------------------------------------------------------------
# Name:        rotowire_daily.py
#
# Author:      aketay
#
# Created:     07/05/2014
# Copyright:   (c) aketay 2014
#-------------------------------------------------------------------------------
from lxml import html
from fuzzywuzzy import fuzz

import requests
import teamDict
import getESPNDict
import time
import csv


page = requests.get('http://www.rotowire.com/baseball/daily_lineups.htm')
tree = html.fromstring(page.text)

colnum = int(tree.xpath('count(/html/body/div[3]/div[1]/div)'))
teamList =[]
team = {}
matchup = []
espnTeamList = []




for c in range (5,colnum):

    for y in range (1,4):

        for x in range (1,3):
            try:
                currentTeam = tree.xpath('/html/body/div[3]/div[1]/div[{}]/div[{}]/div[2]/div[1]/div[{}]/a/text()'.format(c,y,x))
                if x == 1:
                    tempTeam = currentTeam
                else:
                    matchup.append([tempTeam,currentTeam])

            except:
                pass
            team = {}
            try:
                team["P"] = tree.xpath('/html/body/div[3]/div[1]/div[{}]/div[{}]/div[2]/div[2]/div[3]/div[1]/div[{}]/a/text()'.format(c,y,x))[0]
            except:
                pass
            try:
                team["Time"] = tree.xpath('/html/body/div[3]/div[1]/div[{}]/div[{}]/div[1]/div[2]/div[1]/a/text()'.format(c,y))[0]
            except:
                pass
            for i in range(1,10):
                try:
                    team[i] = tree.xpath('/html/body/div[3]/div[1]/div[{}]/div[{}]/div[2]/div[2]/div[{}]/div[{}]/div[2]/a/text()'.format(c,y,x,i))[0]

                except:

                    pass
            try:

                teamList.append({str(currentTeam[0]):team})
            except:
                pass

testDictClass= teamDict.GetTeams()
getESPNDataClass = getESPNDict.GetData()



for item in matchup:
    if item[0] and item[1]:

        #adds abbreviations
        try:
            espnTeamList.append(testDictClass.teamAbbreviationDict[item[0][0]])
            espnTeamList.append(testDictClass.teamAbbreviationDict[item[1][0]])
        except:
            pass



for item in espnTeamList:
    getESPNDataClass.getTeamRoster(item)

getESPNDataClass.writeFinalPlayerInfo()

for item in teamList:
    for team in item.keys():
        for positions in item[team].keys():
            for espnName in getESPNDataClass.playerIDDict.keys():
                if fuzz.ratio(espnName,item[team][positions]) > 85:
                    item[team].update({positions:getESPNDataClass.playerIDDict[espnName]})

for item in matchup:
    if item[0] and item[1]:

        for thing in teamList:
            for team in thing.keys():
                if team == item[0][0]:
                    leftTeam = thing[team]
                if team == item[1][0]:
                    rightTeam = thing[team]

        leftTeamReliefPitchers = getESPNDataClass.getReliefPitchers(testDictClass.teamAbbreviationDict[item[0][0]])
        rightTeamReliefPitchers = getESPNDataClass.getReliefPitchers(testDictClass.teamAbbreviationDict[item[1][0]])

        f = open(r'/Users/Aketay/Desktop/Games/{0}-{1}-{2}.csv'.format(item[0][0],item[1][0],rightTeam["Time"]), 'w')
        try:
            tempRow1 = ["Starting Pitcher",leftTeam["P"],rightTeam["P"]]
            tempRow2 = ["7th",leftTeamReliefPitchers["7th"],rightTeamReliefPitchers["7th"]]
            tempRow3 = ["8th",leftTeamReliefPitchers["8th"],rightTeamReliefPitchers["8th"]]
            tempRow4 = ["9th",leftTeamReliefPitchers["9th"],rightTeamReliefPitchers["9th"]]
            tempRow5 = ["Closer",leftTeamReliefPitchers["Closer"],rightTeamReliefPitchers["Closer"]]
            tempRow6 = ["1",leftTeam[1],rightTeam[1]]
            tempRow7 = ["2",leftTeam[2],rightTeam[2]]
            tempRow8 = ["3",leftTeam[3],rightTeam[3]]
            tempRow9 = ["4",leftTeam[4],rightTeam[4]]
            tempRow10 = ["5",leftTeam[5],rightTeam[5]]
            tempRow11 = ["6",leftTeam[6],rightTeam[6]]
            tempRow12 = ["7",leftTeam[7],rightTeam[7]]
            tempRow13 = ["8",leftTeam[8],rightTeam[8]]
            tempRow14 = ["9",leftTeam[9],rightTeam[9]]
            tempRow15 = ["location",testDictClass.teamAbbreviationDict[item[1][0]],""]
        except:
            pass


        wr = csv.writer(f, dialect='excel')
        wr.writerow(tempRow1)
        wr.writerow(tempRow2)
        wr.writerow(tempRow3)
        wr.writerow(tempRow4)
        wr.writerow(tempRow5)
        wr.writerow(tempRow6)
        wr.writerow(tempRow7)
        wr.writerow(tempRow8)
        wr.writerow(tempRow9)
        wr.writerow(tempRow10)
        wr.writerow(tempRow11)
        wr.writerow(tempRow12)
        wr.writerow(tempRow13)
        wr.writerow(tempRow14)
        wr.writerow(tempRow15)

        f.close()


