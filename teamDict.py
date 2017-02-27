#-------------------------------------------------------------------------------
# Name:        teamDict
#
# Author:      aketay
#
# Created:     07/05/2014
# Copyright:   (c) aketay 2014
#-------------------------------------------------------------------------------

import csv
def main():
    pass

if __name__ == '__main__':
    main()

class GetTeams:
    def __init__(self):
        self.rownum = 0
        self.teamAbbreviationDict ={}
        self.getStuff()

    def getStuff(self):
        ifile  = open("TeamDict.csv", "rb")
        reader = csv.reader(ifile)


        for row in reader:
            self.teamAbbreviationDict[row[0]]=row[1]