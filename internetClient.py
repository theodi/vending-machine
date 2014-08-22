#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib
import urllib2
import time
import socket
import re
import string
from BeautifulSoup import BeautifulStoneSoup  ### nice HTML parser ####

#### Setting some constants #####

###  ENTER KEYWORDS HERE WINDY COMPUTER ###############################
kwords = ['administration', 'administrators', 'bailout', 'bail-out', 'bank', 'bankruptcy', 'banks', 'barclays', 'bill', 'bills', 'bn', 'bonus', 'bonuses', 'boost', 'borrowed', 'borrowing', 'borrows', 'budget', 'budgeting', 'budgets', 'business', 'businesses', 'capital', 'capitalism', 'cash', 'chancellor', 'citigroup', 'city', 'close', 'closes', 'closures', 'contract', 'contracts', 'costs', 'credit', 'crises', 'crisis', 'crunch', 'cut', 'cuts', 'debt', 'debts', 'decline', 'declines', 'deflation', 'dollar', 'dollars', 'dow', 'downturn', 'earn', 'earnings', 'economic', 'economics', 'economies', 'economise', 'economy', 'employed', 'employees', 'employers', 'employment', 'equities', 'equity', 'euro', 'eurozone', 'exchange', 'exchanges', 'exchequer', 'expenses', 'export', 'exports', 'figures', 'finance', 'finances', 'financial', 'firm', 'firms', 'fiscal', 'fiscus', 'forecast', 'forecasts', 'ftse', 'fund', 'funding', 'funds', 'gbp', 'gdp', 'globalisation', 'gloom', 'growth', 'hbos', 'hm treasury', 'house', 'houses', 'housing', 'hsbc', 'hyperinflation', 'hyper-inflation', 'imf', 'import', 'imports', 'income', 'inflation', 'insurers', 'interest', 'investment', 'investments', 'investor', 'investors', 'job', 'job', 'jobless', 'jobs', 'labour', 'lending', 'liquidated', 'liquidation', 'loan', 'loaned', 'loans', 'loss', 'losses', 'managers', 'manufacturer', 'manufacturers', 'manufacturing', 'market', 'markets', 'meltdown', 'money', 'mortgage', 'mortgages', 'nasdaq', 'nationalisation', 'nationalised', 'natwest', 'negative', 'neoliberal', 'neoliberalism', 'osborne', 'output', 'outputs', 'pay', 'payday', 'payment', 'payments', 'pension', 'pensions', 'pinch', 'pound', 'pounds', 'poverty', 'price', 'prices', 'privatisation', 'privatised', 'profit', 'profits', 'properties', 'property', 'rate', 'rates', 'rbs', 'recession', 'recessions', 'recoveries', 'recovery', 'repossessed', 'repossession', 'repossessions', 'retail', 'risk', 'risks', 'sale', 'sales', 'saving', 'savings', 'share', 'shares', 'shoppers', 'shopping', 'slowdown', 'slump', 'slumps', 'spending', 'squeeze', 'sterling', 'stimulate', 'stimuli', 'stimulus', 'stock', 'stocks', 'store', 'stores', 'struggle', 'struggles', 'struggling', 'subsidies', 'subsidy', 'tax', 'taxes', 'trade', 'traded', 'trades', 'trading', 'treasury', 'unemployed', 'unemployment', 'union', 'unions', 'usd', 'wage', 'wages', 'worker', 'workers', 'workforce', 'wto', 'yen'] # << these must all be lowercase
feeddelay = 60 # <----- change this number to set the time between each title being processed
########################################################
########################################################
####  Socket info stuff
recPort = 28910
sendPort = 28911
host = 'localhost'
TBSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#### Constants all set, lets move on ####

######XML parsing
def checkKeyword(word, keylist):
    #print word
    #print keylist
    word = word.lower()
    for item in keylist:
        if item == word:
            return 1

def checkrep(testitem, testlist):
    #print testitem
    #print testlist
    testflag = "new "
    for item in testlist:
        if testitem == item:
            testflag = "rep "
            break
        else:
            testflag ="new "
            
    return testflag
            

def titleParse(doc):
    """ requires beauty """
    soup = BeautifulStoneSoup(doc)
    butter = soup.findAll('title')
    #print "butter is "
    #print butter
    return butter

#def dateParse(doc):
#   """ requires beauty """
#    soup = BeautifulStoneSoup(doc)
#   butter = soup.findAll('pubdate')
#    print "butter is "
#    print butter
#   return butter

#def getTitle(title):
#    #print title
#    #print type(title)
#    title = title.split()
#    print title

################################################################
################################################################

mySocket = socket.socket ( socket.AF_INET, socket.SOCK_DGRAM )
mySocket.bind ( ( '', recPort ) )
TBSock.connect(('localhost',2891))
title2 = []
replist = []
flagercount = 0
flag = 0

while True:
    data, client = mySocket.recvfrom ( 100 )
    data = data.replace(";", "")
    try:
        f = urllib2.urlopen(data)
    except urllib2.URLError:
        print "WARNING: trouble getting data. If this continues please restart."
        print "Will try again in 2 minutes."
        title2 = []
        time.sleep(120)
        ##titlemsg = []
        titlemsg = 'NEWSTIT 10 0 0 starting over;'
        TBSock.send(titlemsg)
        print titlemsg
    else:
        print "getting data ..."
        f = f.read()
        ##f = f.lower()
        soup = BeautifulStoneSoup(f)
        bigtitle = soup.findAll('title')
        
        pubdate = soup.findAll('pubdate')
        del bigtitle [0:2]
        title = bigtitle[0:11]
        if title2 != title:
            print "new feed detected"
            feedcount = 0
            flager ="0 "
            flagerint = 0
            repflager = "new "
            for item in title:
                #print feedcount
                feedstring = str(feedcount)
                item = str(item)
                item = item.replace("£", "GBP ")
                newSoup = BeautifulStoneSoup(item)
                newitem = newSoup.title.contents
                #print type(newitem)
                #newitem2 = str(newitem)
                newitem2 = newitem[0]
                #newitem2 = str(newitem2)
                newitem2 = unicode(newitem2,)
                newitem2 = newitem2.replace(",", "")
                newitem2 = newitem2.replace("$", "USD ")
                newitem2 = newitem2.replace("&amp;", "&")
                #print newitem2
                #print type(newitem2)
                #newitem2 = unicode(newitem2, 'iso_8859_1')
                #newitem2 = newitem2.decode('iso_8859_1')
                newitem = newitem2.split()
                datecont = pubdate[feedcount]
                ##print datecont
                datecont = str(datecont)
                datecont = string.replace(datecont, '<pubdate>', '')
                datecont = string.replace(datecont, '</pubdate>', '')
                datecont = string.replace(datecont, ',', '', 1)
                datecont = string.capwords(datecont)
                datecont = string.replace(datecont, 'Gmt', 'GMT', 1)
                datecont = string.replace(datecont, 'Bst', 'BST', 1)
                datemsg = []
                datemsg = 'PUB ' + datecont + ';'
                ##print datemsg
                for item in newitem:
                    flag = checkKeyword(item, kwords)
                    if flag == 1:
                        break
                if flag == 1:
                    flager = '1 '
                    flagerint = 1
                    repflager = checkrep(newitem2, replist)
                if flagerint == 1 and flag == 1:
                    flagercount = flagercount + 1
                    flagerstring = str(flagercount)
                    cmdstring = "/nd201 /c1001 1 " + flagerstring + " " + "/et"
                    try:
                        msgdata = urllib.urlencode( {'msg' : cmdstring} )
                        url2891 = "http://www.twentyeightninetyone.net/switchboard/switch.php?"
                        fullurl2891 = url2891 + msgdata
                        GS = urllib2.urlopen(fullurl2891)
                        print "2891 responds: 1"
                    except urllib2.URLError:
                        print "2891 is broken!  The greenscreen ain't gonna work. (this time)"
                    #print "flagged!"
                datemsg = []
                datemsg = 'PUB ' + feedstring + " " + repflager  + flager + datecont + ';'        
                titlemsg =[]
                titlemsg = 'NEWSTIT ' + feedstring + " " + repflager + flager + newitem2 + ';'
                titlemsg = titlemsg.encode('utf-8') ## <<- This is needed to send the string over the socket
                print titlemsg
                print datemsg
                #print type(titlemsg)
                TBSock.send(titlemsg)
                TBSock.send(datemsg)
                feedcount = feedcount + 1
                flag = 0
                flager = "0 "
                flagerint = 0
                replfager = "new "
                title2 = title
                
                    
                time.sleep(feeddelay)
                try:
                    msgdata = urllib.urlencode( {'msg' : "/nd201 /c1001 0 /et"} )
                    url2891 = "http://www.twentyeightninetyone.net/switchboard/switch.php?"
                    fullurl2891 = url2891 + msgdata
                    GS = urllib2.urlopen(fullurl2891)
                    print "2891 0"
                except urllib2.URLError:
                    print "2891 is broken!  The greenscreen ain't gonna work. (this time)"
            print "getting new list"    
            replist = []
            for item in title:
                repitem = str(item)
                repSoup = BeautifulStoneSoup(repitem)
                newrepitem = repSoup.title.contents
                #print type(newitem)
                #newitem2 = str(newitem)
                newrepitem2 = newrepitem[0]
                #newitem2 = str(newitem2)
                newrepitem2 = unicode(newrepitem2)
                replist.append(newrepitem2)
                #print replist
        else:
            print "No new feeds found. Ready to try again."
            time.sleep(120)
            titlemsg = []
            titlemsg = 'NEWSTIT 10 0 0 starting over;'
            TBSock.send(titlemsg)
            print titlemsg
    #print titles
    #print type(titles)
    #pdate = dateParse(f)
    #TBSock.send(parsed)


#################################################################
