# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 11:21:25 2016

@author: Dawn Jacob
"""

# -*- coding: utf-8 -*-
"""
Created on Wed May 20 13:22:29 2015
@author: Don
"""

#! /usr/bin/python

import datetime
import time
import csv
import smtplib
import os, sys
import itertools

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def processData():
    
    ordersDataList = []
    
    ordersDataList.append(getListingCount("H"))   #HourlyListingCount
    ordersDataList.append(getListingCount("U"))   #ListingCountbyLister
    ordersDataList.append(getListingCount("D"))   #DailyListingCount
      
    emailSubject = constructEmail("S",ordersDataList)
    emailBody    = constructEmail("B",ordersDataList)
    
    sendEmail(emailSubject,emailBody)
        
    os.remove(partialfilename+"Clean.csv")
    
    return

def cleanData():
      
    lstngTimeStampPrev = " "
        
    fib1  = open(partialfilename+".csv")    
    fi_b1 = csv.reader(fib1)
    
    fob1  = open(partialfilename+"Clean.csv",'w')
    fo_b1 = csv.writer(fob1,lineterminator='\n')

    for row1 in fi_b1:
        
        if row1[3] == lstngTimeStampPrev:
            x = 0
        else:
            lstngTimeStampPrev = row1[3]
            fo_b1.writerow(row1)

    fib1.close()
    fob1.close()
        
    return 
    
def getListingCount(DayOrHour):

    partialfilename = "C:\myFolder\StockChange"
    columnSKU       = 0
    columnStkNow    = 1
    columnLvlChg    = 2
    columnDate      = 3
    columnLstr      = 4
    columnImgId     = 5
    actDay          = 7
    formatAs        = "   -   "
       
    today = datetime.datetime.today()
    thisHour = datetime.datetime.now().strftime('%I')    
    
    two_hours_ago = datetime.datetime.now() - datetime.timedelta(hours=2)
    d = modification_date(partialfilename+".csv")
    
    if d < two_hours_ago :
        return "                                                          Restart Linnworks ---------> " + partialfilename + ".csv is not current \n\n" 

    if DayOrHour == "H":
        filenameSuffix  = "Hr"
    else:
        filenameSuffix  = ""

    customerReturn = 0
    
    fib1  = open(partialfilename+"Clean.csv")    
    fi_b1 = csv.reader(fib1)
    next (fi_b1)
    
    fob1  = open(partialfilename+filenameSuffix+"Tmp.csv",'w')
    fo_b1 = csv.writer(fob1,lineterminator='\n')

    for row1 in fi_b1:
        lstngDte = row1[columnDate].split(" ")[0]
        lstngHr  = row1[columnDate].split(" ")[1].split(":")[0]
        lstrId   = row1[columnLstr]
        lvlChg   = row1[columnLvlChg]
        itemImg  = row1[columnImgId]
    
        if DayOrHour == "H":
            if (((today - datetime.datetime.strptime(lstngDte, '%Y-%m-%d')).days) == 0):
                if lstrId.startswith("Customer Return") :
                    customerReturn = customerReturn + 1
                else:
                    fo_b1.writerow([lstngHr,lvlChg,itemImg])
        elif DayOrHour == "D":
            if lstrId.startswith("Customer Return") :
                customerReturn = customerReturn + 1
            else:
                fo_b1.writerow([lstngDte,lvlChg,itemImg])
        elif DayOrHour == "U":
            if (((today - datetime.datetime.strptime(lstngDte, '%Y-%m-%d')).days) == 0):            
                if lstrId.startswith("Customer Return") :
                    customerReturn = customerReturn + 1
                else:
                    fo_b1.writerow([lstrId,lvlChg,itemImg])
                
    fib1.close()
    fob1.close()
     
    sortLinesInFile(partialfilename+filenameSuffix+"Tmp.csv")
    
    fi = open(partialfilename+filenameSuffix+"Tmp.csv")
    fo = open(partialfilename+filenameSuffix+"Cnt.csv",'w')
    with fi as input, fo as output:  
        reader = csv.reader(input)
        writer = csv.writer(output)
        for column1, row in itertools.groupby(reader, lambda x: x[0]):
            iterLvlChg, iterItmImg = itertools.tee(row)
            lvlChgLst = [x[1] for x in iterLvlChg]
            lvlChgCnt = len(lvlChgLst)
            itmImgLst = [x[2] for x in iterItmImg if x[2] == ""]
            itmImgCnt = len(itmImgLst)
            if DayOrHour == "H":
                UsTimeHour = int(column1) - 5
                if (UsTimeHour >= 12):
                    if (UsTimeHour > 12):
                        UsTimeHour12hrformat = str(UsTimeHour-12).zfill(2) + "-" + str(UsTimeHour-12 + 1).zfill(2) + " PM"
                    elif (UsTimeHour == 12):
                        UsTimeHour12hrformat = str(UsTimeHour) + "-01 PM"
                else:
                    UsTimeHour12hrformat = str(UsTimeHour).zfill(2) + "-" + str(UsTimeHour + 1).zfill(2) + " AM"
                    
                writer.writerow([UsTimeHour12hrformat,lvlChgCnt,itmImgCnt])
            elif DayOrHour == "D":
                dayNum = (today - datetime.datetime.strptime(column1, '%Y-%m-%d')).days
                if dayNum < actDay:
                    while dayNum != actDay  :
                        if actDay < (datetime.datetime.today().weekday()+2):
                            writer.writerow([datetime.datetime.strftime((today - datetime.timedelta(days=actDay)),'%Y-%m-%d'),0,0])
                        actDay = actDay - 1  
                if dayNum == actDay and actDay < (datetime.datetime.today().weekday()+2) :
                    writer.writerow([column1,lvlChgCnt,itmImgCnt])
                    actDay = actDay - 1   
            elif DayOrHour == "U":
                if column1.split("DIRECT ADJUSTMENT BY",1)[0]:
                    writer.writerow([lvlChgCnt,"     (These SKUs are listed first time. Linnworks does not log the userid when stock level is changed very first time for an item - Ticket # 1068233)",itmImgCnt])
                else:
                    writer.writerow([lvlChgCnt,column1.split("DIRECT ADJUSTMENT BY",1)[1],itmImgCnt])
    
    fi.close()
    fo.close()                
    os.remove(partialfilename+filenameSuffix+"Tmp.csv")
    
    lines = ""
    f = open(partialfilename+filenameSuffix+"Cnt.csv", "r")
    for i, line in enumerate(f):
        if line.strip():
            itmImgCnt = line.split(",")[2]
            if DayOrHour == "H":
                lines = lines + "        " + line.split(",")[0] + formatAs + line.split(",")[1].zfill(3) + "\n"
            elif DayOrHour == "U":
                lines = lines + "                             " + line.split(",")[0] + formatAs + line.split(",")[1].zfill(2) + "\n"
            elif DayOrHour == "D":
                if itmImgCnt == "0\n":
                    lines = lines + "                                                    " + line.split(",")[0] + formatAs + line.split(",")[1].zfill(3) + "\n"
                else: 
                    lines = lines + "                                                    " + line.split(",")[0] + formatAs + line.split(",")[1].zfill(3) + "               " + formatAs + "Pending pictures = " + line.split(",")[2].zfill(3)
    f.close()

    os.remove(partialfilename+filenameSuffix+"Cnt.csv")
    #os.startfile("C:/myFolder/OpenOrdersFactoryCnt.csv", "print")
    
    return lines

    
def sortLinesInFile(fileName):
    f = open(fileName, "r")
    lines = [line for line in f if line.strip()]
    f.close()
    lines.sort()
       
    f = open(fileName, 'w')
    f.writelines(lines)
    f.close()    

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)
    
def constructEmail(emailSubjectOrBody,ordersDataList):   
    today    = datetime.date.today().strftime('%x')
    thisHour = datetime.datetime.now().strftime('%I:%M:%S %p')
    now_time = datetime.datetime.now()
    
    if   emailSubjectOrBody == "S" and now_time > now_time.replace(hour=9, minute=0, second=0, microsecond=0) :
        return "Listing Summary : " + str(today) + "  " + str(thisHour) 
               
    elif emailSubjectOrBody == "B" and now_time > now_time.replace(hour=9, minute=0, second=0, microsecond=0) :
        body =        "PAYLESS COMPONENTS : \n******************\n" 
        body = body + "        Listings by the Hour today: \n" + ordersDataList[0] + "\n"
        body = body + "                             Listings per Lister today: \n" + ordersDataList[1] + "\n\n"        
        body = body + "                                                    Daily Listings this week starting Sunday: \n" + ordersDataList[2] + "\n\n"
        body = body + "NOTE: This report does NOT exclude boards that are listed but WAITING for pictures to be taken. So please ensure that all pending pictures are taken BEFORE End of Day."
        return body 
    
def sendEmail(emailSubject,emailBody):
    me = "reports@paylesscomponents.com"
    you = "don@paylesscomponents.com"
    #you = ["don@paylesscomponents.com", "sales@paylesscomponents.com"]
    #you = ["kyle@paylesscomponents.com", "don@paylesscomponents.com", "nick@paylesscomponents.com"]
    #you = ["kyle@paylesscomponents.com", "jhamamy@factory-surplus.com", "nick@paylesscomponents.com", "DeAndre@paylesscomponents.com", "don@paylesscomponents.com"]
    
    COMMASPACE = ', '

    msg = MIMEMultipart('alternative')
    msg['Subject'] = emailSubject
    msg['From'] = me
    msg['To'] = COMMASPACE.join(you)

    part1 = MIMEText(emailBody, 'plain')       
    msg.attach(part1)
    
    s = smtplib.SMTP_SSL('smtpout.secureserver.net',465)       
    s.login("don@paylesscomponents.com", "donpay123")
    
    s.sendmail(me, you, msg.as_string())
    s.quit()

cleanData()

processData()