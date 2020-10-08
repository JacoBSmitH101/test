import requests
from bs4 import BeautifulSoup
import os
import time
import datetime

def getCnmInfoNow():
    now = datetime.datetime.now()
    day = None
    if not len(str(datetime.datetime.today().day)) == 2:
        day = '0' + str(datetime.datetime.today().day)
    else:
        day = datetime.datetime.today().day
    if not len(str(datetime.datetime.today().hour)) == 2:
        hour = '0' + str(datetime.datetime.today().hour)
    else:
        hour = datetime.datetime.today().hour
    if not len(str(datetime.datetime.today().minute)) == 2:
        minute = '0' + str(datetime.datetime.today().minute)
    else:
        minute = datetime.datetime.today().minute
    url = 'https://www.realtimetrains.co.uk/search/detailed/CNM/' + str(datetime.datetime.today().year) + '-' + str(datetime.datetime.today().month) + '-' + str(day) + '/' + str(hour) + str(minute)
    print(url)
    print(str(datetime.datetime.today().year))
    res = requests.get(url)
    html_page = res.content

    soup = BeautifulSoup(html_page, 'html.parser')
    # start = str(soup.find(' '))
    # print(str(soup))
    # print(start)
    one_a_tag = soup.findAll('a')
    print(one_a_tag)

    f = open("html.txt", "w")
    newsoup = str(soup).replace('\u21e3', '')
    newsoup = newsoup.replace('\u21e1', '')
    f.write(newsoup[12337:25500])
    f.close()
    
    page = open("html.txt", "r")
    cursorPos = 0
    bad_words = ['nonpax']
    try:
        os.remove('output.txt')
    except:
        ouput = open('output.txt', 'w')
    with open('html.txt') as oldfile, open('nonpax.txt', 'w') as newfile:
        for line in oldfile:
            if any(bad_word in line for bad_word in bad_words):
                newfile.write(line)

    with open("nonpax.txt", 'r') as original, open("output.txt", 'w') as completed:
        for line in original:
            cursorPos = 0
            cursorPos+=10
            foundLink=False
            while foundLink == False:
                if line[cursorPos] == '=':
                    foundLink = True
                else:
                    cursorPos+=1
            cursorPos += 2
            startLinkPos = cursorPos
            foundLink=False
            while foundLink == False:
                if line[cursorPos] == '>':
                    foundLink = True
                else:
                    cursorPos+=1
            cursorPos-=1
            link = 'https://www.realtimetrains.co.uk' + line[startLinkPos:cursorPos]
            cursorPos+=1

            foundType = False
            while foundType == False:
                if line[cursorPos].isupper():
                    foundType = True
                else:
                    cursorPos+=1


            if line[cursorPos:cursorPos+3] == 'WTT':
                cursorPos+=4

                if line[cursorPos:cursorPos+35].find('time plan a pass') > 1 or line[cursorPos:cursorPos+35].find('time plan a ts') > 1:
                    #ones without time at start
                    foundArrival = False

                    while foundArrival == False:
                        if line[cursorPos].isupper():
                            foundArrival = True
                        else:
                            cursorPos+=1
                    startPos = cursorPos
                    foundArrival = False
                    while foundArrival == False:
                        if line[cursorPos] == '<':
                            foundArrival = True
                        else:
                            cursorPos+=1

                    departureLocation = line[startPos:cursorPos]

                    foundPlatform = False
                    while foundPlatform == False:
                        if line[cursorPos].isdigit():
                            foundPlatform = True
                        else:
                            cursorPos+=1
                    platform = line[cursorPos]

                    cursorPos+=1
                    foundHeadcode = False
                    while foundHeadcode == False:
                        if line[cursorPos].isdigit() or line[cursorPos] == 'F' and line[cursorPos+1] == 'R':
                            foundHeadcode = True
                        else:
                            cursorPos+=1

                    headcode = line[cursorPos:cursorPos+4]
                    cursorPos+=5

                    foundCompany = False
                    while foundCompany == False:
                        if line[cursorPos].isupper():
                            foundCompany = True
                        else:
                            cursorPos+=1
                    company = line[cursorPos:cursorPos+2]

                    cursorPos+=3

                    foundArrival = False
                    while foundArrival == False:
                        if line[cursorPos].isupper():
                            foundArrival = True
                        else:
                            cursorPos+=1
                    startPos = cursorPos
                    foundArrival = False
                    while foundArrival == False:
                        if line[cursorPos] == '<':
                            foundArrival = True
                        else:
                            cursorPos+=1
                    arrivalLocation = line[startPos:cursorPos]
                    cursorPos+=2

                    foundPlanTime = False
                    while foundPlanTime == False:
                        if line[cursorPos].isdigit():
                            foundPlanTime = True
                        else:
                            cursorPos+=1
                    timeTableTime = line[cursorPos:cursorPos+4]
                    cursorPos+=5

                    realTimeTime = None
                    if line[cursorPos:].find('time real d c rrq') > 1:
                        realTimeTime = 'Runs as required'
                    elif line[cursorPos:].find('time real d canx') > 1:
                        realTimeTime = 'Cancelled by Train Operator'
                    else:
                        foundRealtime = False
                        while foundRealtime == False:
                            if line[cursorPos].isdigit():
                                foundRealtime = True
                            else:
                                cursorPos+=1
                        realTimeTime = line[cursorPos:cursorPos+4]

                    #output into output.txt
                    completed.write(departureLocation + ' - ' + arrivalLocation + '\n')
                    completed.write('Company: ' + company + '\n')
                    completed.write('Platform: ' + platform + '\n')
                    completed.write('Scheduled Time: ' + timeTableTime + '\n')
                    completed.write('Real Time: ' + realTimeTime + '\n')
                    completed.write('HeadCode: ' + headcode + '\n')
                    completed.write('Link: ' + link + '\n\n')


                elif line[cursorPos:cursorPos+35].find('time plan a wtt') > 1:
                    foundPlanTime = False
                    while foundPlanTime == False:
                        if line[cursorPos].isdigit():
                            foundPlanTime = True
                        else:
                            cursorPos += 1
                    timeTableTime = line[cursorPos:cursorPos + 4]
                    cursorPos += 5

                    realTimeTime = None
                    if line[cursorPos:].find('time real d c rrq') > 1:
                        realTimeTime = 'Runs as required'
                    elif line[cursorPos:].find('time real d canx') > 1:
                        realTimeTime = 'Cancelled by Train Operator'
                    else:
                        foundRealtime = False
                        while foundRealtime == False:
                            if line[cursorPos].isdigit():
                                foundRealtime = True
                            else:
                                cursorPos += 1
                        realTimeTime = line[cursorPos:cursorPos + 4]
                    cursorPos+=5
                    foundArrival = False
                    while foundArrival == False:
                        if line[cursorPos].isupper():
                            foundArrival = True
                        else:
                            cursorPos+=1
                    startPos = cursorPos
                    foundArrival = False
                    while foundArrival == False:
                        if line[cursorPos] == '<':
                            foundArrival = True
                        else:
                            cursorPos+=1

                    departureLocation = line[startPos:cursorPos]

                    foundPlatform = False
                    while foundPlatform == False:
                        if line[cursorPos].isdigit():
                            foundPlatform = True
                        else:
                            cursorPos+=1
                    platform = line[cursorPos]

                    cursorPos+=1
                    foundHeadcode = False
                    while foundHeadcode == False:
                        if line[cursorPos].isdigit() or line[cursorPos] == 'F' and line[cursorPos+1] == 'R':
                            foundHeadcode = True
                        else:
                            cursorPos+=1

                    headcode = line[cursorPos:cursorPos+4]
                    cursorPos+=5

                    foundCompany = False
                    while foundCompany == False:
                        if line[cursorPos].isupper():
                            foundCompany = True
                        else:
                            cursorPos+=1
                    company = line[cursorPos:cursorPos+2]

                    cursorPos+=3

                    foundArrival = False
                    while foundArrival == False:
                        if line[cursorPos].isupper():
                            foundArrival = True
                        else:
                            cursorPos+=1
                    startPos = cursorPos
                    foundArrival = False
                    while foundArrival == False:
                        if line[cursorPos] == '<':
                            foundArrival = True
                        else:
                            cursorPos+=1
                    arrivalLocation = line[startPos:cursorPos]
                    cursorPos+=2


                    #output into output.txt
                    completed.write(departureLocation + ' - ' + arrivalLocation + '\n')
                    completed.write('Company: ' + company + '\n')
                    completed.write('Platform: ' + platform + '\n')
                    completed.write('Scheduled Time: ' + timeTableTime + '\n')
                    completed.write('Real Time: ' + realTimeTime + '\n')
                    completed.write('HeadCode: ' + headcode + '\n')
                    completed.write('Link: ' + link + '\n\n')

            elif line[cursorPos:cursorPos+3] == 'STP' or line[cursorPos:cursorPos+3] == 'VAR':
                cursorPos += 4

                if line[cursorPos:cursorPos + 35].find('time plan a pass') > 1 or line[cursorPos:cursorPos + 35].find(
                        'time plan a ts') > 1:
                    # ones without time at start
                    foundArrival = False

                    while foundArrival == False:
                        if line[cursorPos].isupper():
                            foundArrival = True
                        else:
                            cursorPos += 1
                    startPos = cursorPos
                    foundArrival = False
                    while foundArrival == False:
                        if line[cursorPos] == '<':
                            foundArrival = True
                        else:
                            cursorPos += 1

                    departureLocation = line[startPos:cursorPos]

                    foundPlatform = False
                    while foundPlatform == False:
                        if line[cursorPos].isdigit():
                            foundPlatform = True
                        else:
                            cursorPos += 1
                    platform = line[cursorPos]

                    cursorPos += 1
                    foundHeadcode = False
                    while foundHeadcode == False:
                        if line[cursorPos].isdigit() or line[cursorPos] == 'F' and line[cursorPos + 1] == 'R':
                            foundHeadcode = True
                        else:
                            cursorPos += 1

                    headcode = line[cursorPos:cursorPos + 4]
                    cursorPos += 5

                    foundCompany = False
                    while foundCompany == False:
                        if line[cursorPos].isupper():
                            foundCompany = True
                        else:
                            cursorPos += 1
                    company = line[cursorPos:cursorPos + 2]

                    cursorPos += 3

                    foundArrival = False
                    while foundArrival == False:
                        if line[cursorPos].isupper():
                            foundArrival = True
                        else:
                            cursorPos += 1
                    startPos = cursorPos
                    foundArrival = False
                    while foundArrival == False:
                        if line[cursorPos] == '<':
                            foundArrival = True
                        else:
                            cursorPos += 1
                    arrivalLocation = line[startPos:cursorPos]
                    cursorPos += 2

                    foundPlanTime = False
                    while foundPlanTime == False:
                        if line[cursorPos].isdigit():
                            foundPlanTime = True
                        else:
                            cursorPos += 1
                    timeTableTime = line[cursorPos:cursorPos + 4]
                    cursorPos += 5

                    realTimeTime = None
                    if line[cursorPos:].find('time real d c rrq') > 1:
                        realTimeTime = 'Runs as required'
                    elif line[cursorPos:].find('time real d canx') > 1:
                        realTimeTime = 'Cancelled by Train Operator'
                    else:
                        foundRealtime = False
                        while foundRealtime == False:
                            if line[cursorPos].isdigit():
                                foundRealtime = True
                            else:
                                cursorPos += 1
                        realTimeTime = line[cursorPos:cursorPos + 4]

                    # output into output.txt
                    completed.write(departureLocation + ' - ' + arrivalLocation + '\n')
                    completed.write('Company: ' + company + '\n')
                    completed.write('Platform: ' + platform + '\n')
                    completed.write('Scheduled Time: ' + timeTableTime + '\n')
                    completed.write('Real Time: ' + realTimeTime + '\n')
                    completed.write('HeadCode: ' + headcode + '\n')
                    completed.write('Link: ' + link + '\n\n')


                elif line[cursorPos:cursorPos + 35].find('time plan a wtt') > 1:
                    foundPlanTime = False
                    while foundPlanTime == False:
                        if line[cursorPos].isdigit():
                            foundPlanTime = True
                        else:
                            cursorPos += 1
                    timeTableTime = line[cursorPos:cursorPos + 4]
                    cursorPos += 5

                    realTimeTime = None
                    if line[cursorPos:].find('time real d c rrq') > 1:
                        realTimeTime = 'Runs as required'
                    elif line[cursorPos:].find('time real d canx') > 1:
                        realTimeTime = 'Cancelled by Train Operator'
                    else:
                        foundRealtime = False
                        while foundRealtime == False:
                            if line[cursorPos].isdigit():
                                foundRealtime = True
                            else:
                                cursorPos += 1
                        realTimeTime = line[cursorPos:cursorPos + 4]
                    cursorPos += 5
                    foundArrival = False
                    while foundArrival == False:
                        if line[cursorPos].isupper():
                            foundArrival = True
                        else:
                            cursorPos += 1
                    startPos = cursorPos
                    foundArrival = False
                    while foundArrival == False:
                        if line[cursorPos] == '<':
                            foundArrival = True
                        else:
                            cursorPos += 1

                    departureLocation = line[startPos:cursorPos]

                    foundPlatform = False
                    while foundPlatform == False:
                        if line[cursorPos].isdigit():
                            foundPlatform = True
                        else:
                            cursorPos += 1
                    platform = line[cursorPos]

                    cursorPos += 1
                    foundHeadcode = False
                    while foundHeadcode == False:
                        if line[cursorPos].isdigit() or line[cursorPos] == 'F' and line[cursorPos + 1] == 'R':
                            foundHeadcode = True
                        else:
                            cursorPos += 1

                    headcode = line[cursorPos:cursorPos + 4]
                    cursorPos += 5

                    foundCompany = False
                    while foundCompany == False:
                        if line[cursorPos].isupper():
                            foundCompany = True
                        else:
                            cursorPos += 1
                    company = line[cursorPos:cursorPos + 2]

                    cursorPos += 3

                    foundArrival = False
                    while foundArrival == False:
                        if line[cursorPos].isupper():
                            foundArrival = True
                        else:
                            cursorPos += 1
                    startPos = cursorPos
                    foundArrival = False
                    while foundArrival == False:
                        if line[cursorPos] == '<':
                            foundArrival = True
                        else:
                            cursorPos += 1
                    arrivalLocation = line[startPos:cursorPos]
                    cursorPos += 2

                    # output into output.txt
                    completed.write(departureLocation + ' - ' + arrivalLocation + '\n')
                    completed.write('Company: ' + company + '\n')
                    completed.write('Platform: ' + platform + '\n')
                    completed.write('Scheduled Time: ' + timeTableTime + '\n')
                    completed.write('Real Time: ' + realTimeTime + '\n')
                    completed.write('HeadCode: ' + headcode + '\n')
                    completed.write('Link: ' + link + '\n\n')




def getAnyInfoAnyTime(place, date, time):
    print("NO")
    print("OTHER TEST")


