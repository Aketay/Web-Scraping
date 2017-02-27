#-------------------------------------------------------------------------------
# Name:        getESPNDict
#
# Author:      aketay
#
# Created:     07/05/2014
# Copyright:   (c) aketay 2014
#-------------------------------------------------------------------------------
from lxml import html
import requests
import re
import time
import csv

class GetData:
    def __init__(self):
        self.playerIDDict = {}
        self.rownum = 0
        self.playerIDDict = {}


    def getTeamRoster(self,s):
        websiteString = "http://espn.go.com/mlb/team/roster/_/name/" + s

        page = requests.get(websiteString)
        tree = html.fromstring(page.text)
        self.rownum = int(tree.xpath('count(//*[@id="my-players-table"]/div[3]/div[1]/div[1]/div/table[1]/tr)'))
        time.sleep(1)

        for i in range (1,self.rownum):
            try:
               self.playerIDDict.update({tree.xpath('//*[@id="my-players-table"]/div[3]/div[1]/div[1]/div/table[1]//tr[{}]/td[2]/a/text()'.format(i))[0] : re.sub("\D","",str(tree.xpath('//*[@id="my-players-table"]/div[3]/div[1]/div[1]/div/table[1]//tr[{}]/td[2]/a/@href'.format(i))[0]))})
            except:
                pass

    def writeFinalPlayerInfo(self):
        f = open(r'/Users/Aketay/Desktop/ESPNPlayerList.csv', 'w')

        for item in self.playerIDDict.keys():
            tempRow = [item,self.playerIDDict[item]]
            wr = csv.writer(f, dialect='excel')
            wr.writerow(tempRow)

        f.close()

    def getReliefPitchers(self,s):
        websiteString = "http://espn.go.com/mlb/team/depth/_/name/" + s

        page = requests.get(websiteString)
        tree = html.fromstring(page.text)
        colcount = int(tree.xpath('count(//*[@id="my-teams-table"]/div[3]/div/table/tr)')) - 1
        closercol = int(tree.xpath('count(//*[@id="my-teams-table"]/div[3]/div/table/tr)'))

        tempDict = {}
        try:
            tempDict['7th'] = re.sub("\D","",tree.xpath('//*[@id="my-teams-table"]/div[3]/div/table/tr[{}]/td[2]/strong/a/@href'.format(colcount))[0])
        except:
            tempDict['7th'] = ""
        try:
            tempDict['8th'] = re.sub("\D","",tree.xpath('//*[@id="my-teams-table"]/div[3]/div/table/tr[{}]/td[3]/a/@href'.format(colcount))[0])
        except:
            tempDict['8th'] = ""
        try:
            tempDict['9th'] = re.sub("\D","",tree.xpath('//*[@id="my-teams-table"]/div[3]/div/table/tr[{}]/td[4]/a/@href'.format(colcount))[0])
        except:
            tempDict['9th'] = ""

        try:
            tempDict['Closer'] = re.sub("\D","",tree.xpath('//*[@id="my-teams-table"]/div[3]/div/table/tr[{}]/td[2]/strong/a/@href'.format(closercol))[0])
        except:
            tempDict['Closer'] = ""
        return tempDict


