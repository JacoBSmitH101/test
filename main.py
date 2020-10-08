import requests
from bs4 import BeautifulSoup
import os
import time
import datetime
import random
import asyncio
import aiohttp
import json
import discord
from discord import Game
from discord.ext.commands import Bot
from discord.ext import commands






def getInfoStandard():
    now = datetime.datetime.now()
    url = 'https://www.realtimetrains.co.uk/search/detailed/CNM'
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
    print("TESING")
    page = open("html.txt", "r")

    bad_words = ['nonpax']
    try:
        os.remove('output.txt')
    except:
        ouput = open('output.txt', 'w')
    with open('html.txt') as oldfile, open('completed.txt', 'w') as newfile:
        for line in oldfile:
            if any(bad_word in line for bad_word in bad_words):
                newfile.write(line)


    def makeReadable(file):
        for line in file:
            lineString = line
            lineString.replace('class="service', '')


    page = open("completed.txt", "r")

    makeReadable(page)

    with open("completed.txt") as unreadable, open("new.txt", 'w') as completed:
        for line in unreadable:
            line = line.replace('<a class="service nonpax', '')
            line = line.replace('pass', '')
            line = line.replace('"', '')
            line = line.replace(' ', '')
            line = line.replace('origin', '')
            # does contain stp
            if 'STP' in line:
                # line = line[105:]
                cursorPos = 0
                foundLink = False
                while foundLink == False:
                    if line[cursorPos] == '/':
                        foundLink = True
                    else:
                        cursorPos = cursorPos + 1
                linkStartPos = cursorPos

                foundLink = False
                while foundLink == False:
                    if line[cursorPos] == '<':
                        foundLink = True
                    else:
                        cursorPos = cursorPos + 1
                link = 'https://www.realtimetrains.co.uk' + line[linkStartPos:cursorPos - 1]
                foundName = False
                cursorPos = cursorPos + 22
                while foundName == False:
                    if line[cursorPos].isupper():
                        foundName = True
                    else:
                        cursorPos = cursorPos + 1
                depstartname = cursorPos
                foundName = False
                while foundName == False:
                    if line[cursorPos] == '<':
                        foundName = True
                    else:
                        cursorPos = cursorPos + 1
                departureLocation = line[depstartname:cursorPos]
                foundPlatform = False
                while foundPlatform == False:
                    if line[cursorPos].isdigit():
                        foundPlatform = True
                    else:
                        cursorPos = cursorPos + 1
                platform = line[cursorPos]
                cursorPos = cursorPos + 1
                foundHeadcode = False
                while foundHeadcode == False:
                    if line[cursorPos].isdigit():
                        foundHeadcode = True
                    else:
                        cursorPos = cursorPos + 1
                headCode = line[cursorPos:cursorPos + 4]
                cursorPos = cursorPos + 4
                foundCompany = False
                while foundCompany == False:
                    if line[cursorPos].isupper():
                        foundCompany = True
                    else:
                        cursorPos = cursorPos + 1
                company = line[cursorPos] + line[cursorPos + 1]
                cursorPos = cursorPos + 2
                foundArrival = False
                while foundArrival == False:
                    if line[cursorPos].isupper():
                        foundArrival = True
                    else:
                        cursorPos = cursorPos + 1
                startOfArrivalString = cursorPos
                foundArrival = False
                while foundArrival == False:
                    if line[cursorPos] == '<':
                        foundArrival = True
                    else:
                        cursorPos = cursorPos + 1
                arrivalLocation = line[startOfArrivalString:cursorPos]
                foundTime = False
                while foundTime == False:
                    if line[cursorPos].isdigit():
                        foundTime = True
                    else:
                        cursorPos = cursorPos + 1
                timeTableTime = line[cursorPos:cursorPos + 4]
                cursorPos = cursorPos + 4
                foundTime = False
                while foundTime == False:
                    if line[cursorPos].isdigit():
                        foundTime = True
                    else:
                        cursorPos = cursorPos + 1
                realTimeTime = line[cursorPos:cursorPos + 4]

                time.sleep(1)
                ouput = open("output.txt", 'a')
                ouput.write(
                    departureLocation + "-" + arrivalLocation + "\nCompany: " + company + "\nPlatform: " + platform + "\nScheduled Arrival: " + timeTableTime + "\nReal Time arrival: " + realTimeTime + "\nHeadcode: " + headCode + "\nLink: " + link + "\n\n")






            elif 'WTT' in line:
                cursorPos = 0
                foundLink = False
                timeTableTime = None
                realTimeTime = None

                while foundLink == False:
                    if line[cursorPos] == '/':
                        foundLink = True
                    else:
                        cursorPos = cursorPos + 1
                linkStartPos = cursorPos
                foundLink = False
                while foundLink == False:
                    if line[cursorPos] == '<':
                        foundLink = True
                    else:
                        cursorPos = cursorPos + 1
                link = 'https://www.realtimetrains.co.uk' + line[linkStartPos:cursorPos - 1]

                isS = False

                # if S then it starts here if not then get time
                # if line[cursorPos] == "s":
                #     departureLocation = "Cheltenham Spa"
                #     isS = True
                #
                # else:
                #     isS = False
                #     cursorPos = cursorPos + 3
                #     timeTableTime = line[cursorPos:cursorPos + 4]
                #     realTimeTime = 'N/A'
                #     cursorPos = cursorPos + 4
                #     foundTime = False
                #     while foundTime == False:
                #         if line[cursorPos].isdigit():
                #             foundTime = True
                #         else:
                #             cursorPos = cursorPos + 1
                #     realTimeTime = line[cursorPos:cursorPos + 4]
                #     cursorPos = cursorPos + 4

                foundRealTime = False
                foundPlanTime = False

                cursorPos += 30

                # get departure
                foundName = False
                while foundName == False:
                    if line[cursorPos].isupper():
                        foundName = True
                    else:
                        cursorPos = cursorPos + 1
                depstartname = cursorPos
                foundName = False
                while foundName == False:
                    if line[cursorPos] == '<':
                        foundName = True
                    else:
                        cursorPos = cursorPos + 1
                departureLocation = line[depstartname:cursorPos]
                if departureLocation == 'Startshere': departureLocation = 'CheltenhamSpa'
                print(departureLocation)

                foundPlatform = False
                while foundPlatform == False:
                    if line[cursorPos].isdigit():
                        foundPlatform = True
                    else:
                        cursorPos = cursorPos + 1
                platform = line[cursorPos]
                cursorPos = cursorPos + 1

                foundHeadcode = False
                while foundHeadcode == False:
                    if line[cursorPos].isdigit():
                        foundHeadcode = True
                    else:
                        cursorPos = cursorPos + 1
                headCode = line[cursorPos:cursorPos + 4]
                cursorPos = cursorPos + 4

                foundCompany = False
                if cursorPos >= len(line): return

                while foundCompany == False:
                    if line[cursorPos].isupper():
                        foundCompany = True
                    else:
                        cursorPos = cursorPos + 1
                company = line[cursorPos] + line[cursorPos + 1]
                cursorPos = cursorPos + 2
                print(foundCompany)

                foundArrival = False

                while foundArrival == False:
                    if line[cursorPos].isupper():
                        foundArrival = True
                    else:
                        cursorPos = cursorPos + 1
                startOfArrivalString = cursorPos
                if cursorPos >= len(line): return
                foundArrival = False
                while foundArrival == False:
                    if line[cursorPos] == '<':
                        foundArrival = True
                    else:
                        cursorPos = cursorPos + 1
                arrivalLocation = line[startOfArrivalString:cursorPos]
                if cursorPos >= len(line): return
                prevPos = None
                if 'timeplanawtt' in line:
                    prevPos = cursorPos
                    cursorPos = 30
                while foundPlanTime == False:
                    if line[cursorPos].isdigit():
                        foundPlanTime = True
                    else:
                        cursorPos += 1

                timeTableTime = line[cursorPos:cursorPos + 4]
                cursorPos += 5
                while foundRealTime == False:
                    if line[cursorPos].isdigit():
                        foundRealTime = True
                    else:
                        cursorPos += 1
                realTimeTime = line[cursorPos:cursorPos + 4]
                cursorPos += 5
                nextNumber = False
                if prevPos:
                    while nextNumber == False:
                        if line[cursorPos].isdigit():
                            nextNumber = True
                        else:
                            cursorPos += 1
                    cursorPos += 1
                    foundHeadcode = False
                    while foundHeadcode == False:
                        if line[cursorPos].isdigit():
                            foundHeadcode = True
                        else:
                            cursorPos = cursorPos + 1
                    headCode = line[cursorPos:cursorPos + 4]
                    cursorPos = cursorPos + 4

                time.sleep(1)
                if departureLocation == arrivalLocation:
                    departureLocation = 'CheltenhamSpa'
                    arrivalLocation = 'Sidings'
                if departureLocation == 'CheltenhamSpa' and arrivalLocation == 'Terminateshere':
                    departureLocation = 'Siding'
                    arrivalLocation = 'CheltenhamSpa'
                ouput = open("output.txt", 'a')
                if timeTableTime == None: timeTableTime = 'N/A'
                if realTimeTime == None or realTimeTime == '1></': realTimeTime = 'N/A'

                ouput.write(
                    departureLocation + "-" + arrivalLocation + "\nCompany: " + company + "\nPlatform: " + platform + "\nScheduled Arrival: " + timeTableTime + "\nReal Time arrival: " + realTimeTime + "\nHeadcode: " + headCode + "\nLink: " + link + "\n\n")

            elif 'VAR' in line or 'VST' in line:
                cursorPos = 0
                foundLink = False
                timeTableTime = None
                realTimeTime = None

                while foundLink == False:
                    if line[cursorPos] == '/':
                        foundLink = True
                    else:
                        cursorPos = cursorPos + 1
                linkStartPos = cursorPos
                foundLink = False
                while foundLink == False:
                    if line[cursorPos] == '<':
                        foundLink = True
                    else:
                        cursorPos = cursorPos + 1
                link = 'https://www.realtimetrains.co.uk' + line[linkStartPos:cursorPos - 1]

                isS = False

                # if S then it starts here if not then get time
                # if line[cursorPos] == "s":
                #     departureLocation = "Cheltenham Spa"
                #     isS = True
                #
                # else:
                #     isS = False
                #     cursorPos = cursorPos + 3
                #     timeTableTime = line[cursorPos:cursorPos + 4]
                #     realTimeTime = 'N/A'
                #     cursorPos = cursorPos + 4
                #     foundTime = False
                #     while foundTime == False:
                #         if line[cursorPos].isdigit():
                #             foundTime = True
                #         else:
                #             cursorPos = cursorPos + 1
                #     realTimeTime = line[cursorPos:cursorPos + 4]
                #     cursorPos = cursorPos + 4

                foundRealTime = False
                foundPlanTime = False

                cursorPos += 30

                # get departure
                foundName = False
                while foundName == False:
                    if line[cursorPos].isupper():
                        foundName = True
                    else:
                        cursorPos = cursorPos + 1
                depstartname = cursorPos
                foundName = False
                while foundName == False:
                    if line[cursorPos] == '<':
                        foundName = True
                    else:
                        cursorPos = cursorPos + 1
                departureLocation = line[depstartname:cursorPos]
                if departureLocation == 'Startshere': departureLocation = 'CheltenhamSpa'

                foundPlatform = False
                while foundPlatform == False:
                    if line[cursorPos].isdigit():
                        foundPlatform = True
                    else:
                        cursorPos = cursorPos + 1
                platform = line[cursorPos]
                cursorPos = cursorPos + 1

                foundHeadcode = False
                while foundHeadcode == False:
                    if line[cursorPos].isdigit():
                        foundHeadcode = True
                    else:
                        cursorPos = cursorPos + 1
                headCode = line[cursorPos:cursorPos + 4]
                cursorPos = cursorPos + 4

                foundCompany = False

                while foundCompany == False:
                    if line[cursorPos].isupper():
                        foundCompany = True
                    else:
                        cursorPos = cursorPos + 1
                company = line[cursorPos] + line[cursorPos + 1]
                cursorPos = cursorPos + 2

                foundArrival = False
                while foundArrival == False:
                    if line[cursorPos].isupper():
                        foundArrival = True
                    else:
                        cursorPos = cursorPos + 1
                startOfArrivalString = cursorPos
                foundArrival = False
                while foundArrival == False:
                    if line[cursorPos] == '<':
                        foundArrival = True
                    else:
                        cursorPos = cursorPos + 1
                arrivalLocation = line[startOfArrivalString:cursorPos]
                prevPos = None
                if 'timeplanawtt' in line:
                    prevPos = cursorPos
                    cursorPos = 30
                while foundPlanTime == False:
                    if line[cursorPos].isdigit():
                        foundPlanTime = True
                    else:
                        cursorPos += 1

                timeTableTime = line[cursorPos:cursorPos + 4]
                cursorPos += 5
                print('time real a pass' in line)
                while foundRealTime == False and not 'time real a pass' in line:

                    if line[cursorPos].isdigit():
                        foundRealTime = True
                    else:
                        cursorPos += 1
                realTimeTime = line[cursorPos:cursorPos + 4]
                cursorPos += 5
                nextNumber = False
                if prevPos:
                    while nextNumber == False:
                        if line[cursorPos].isdigit():
                            nextNumber = True
                        else:
                            cursorPos += 1
                    cursorPos += 1
                    foundHeadcode = False
                    while foundHeadcode == False:
                        if line[cursorPos].isdigit():
                            foundHeadcode = True
                        else:
                            cursorPos = cursorPos + 1
                    headCode = line[cursorPos:cursorPos + 4]
                    cursorPos = cursorPos + 4

                time.sleep(1)
                if departureLocation == arrivalLocation:
                    departureLocation = 'CheltenhamSpa'
                    arrivalLocation = 'Sidings'
                if departureLocation == 'CheltenhamSpa' and arrivalLocation == 'Terminateshere':
                    departureLocation = 'Siding'
                    arrivalLocation = 'CheltenhamSpa'
                ouput = open("output.txt", 'a')
                if timeTableTime == None: timeTableTime = 'N/A'
                if realTimeTime == None or realTimeTime == '1></': realTimeTime = 'N/A'

                ouput.write(
                    departureLocation + "-" + arrivalLocation + "\nCompany: " + company + "\nPlatform: " + platform + "\nScheduled Arrival: " + timeTableTime + "\nReal Time arrival: " + realTimeTime + "\nHeadcode: " + headCode + "\nLink: " + link + "\n\n")
        try:
            completed.write(line)
        except:
            print("NOT IN FILE")



