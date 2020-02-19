import json
import time
from _datetime import datetime
from operator import itemgetter


# loads json data to memory
def defLoadDate():
    fileName = datetime.today().strftime('JSON_files/%Y_%m_%d') + ".json"       # opening file with today's date by default
    with open(fileName, 'r') as read_date:                                      # opening file with today's date
        dateData = json.load(read_date)                                         # loading data to memory
    return dateData                                                             # returning data


# iterates through whole json file
def defIterateJson(jsonData):
    for k, v in jsonData.items():       # loop through every major object in list
        print(k, v)                     # printing up the data from json
        print('=' * 50)
    return


# function that sums up total usage time for every application, creates dictionary, where applications are keys
# and total time is a value, then it sorts the list in descending order
def defSummingUpTotalTime(jsonData):
    totalTimeForApplication = {}
    totalTimeForAllApps = 0
    for keyNumber in range(len(jsonData)):                                                      # iterating through major applications
        timeTotal = 0                                                                           # defining total time variable
        applicationKey = list(jsonData.keys())                                                  # finding key (application name), which is different for every object
        for instance in range(len(jsonData[applicationKey[keyNumber]])):                        # iterating through instances in every application
            timeTotal += jsonData[applicationKey[keyNumber]][instance]["total"]                 # summimg up time from every instance
        totalTimeForAllApps += timeTotal                                                        # summing up total usage time for all apps
        totalTimeForApplication[applicationKey[keyNumber]] = {}                                 # creating dictionary, where applications are keys and values are total usage times
        totalTimeForApplication[applicationKey[keyNumber]]['Usage time'] = timeTotal
    for keyNumber in range(len(totalTimeForApplication)):
        applicationKey = list(totalTimeForApplication.keys())
        timePercentage = round(totalTimeForApplication[applicationKey[keyNumber]]['Usage time'] / totalTimeForAllApps, 2)
        totalTimeForApplication[applicationKey[keyNumber]]['Percentage time of use'] = timePercentage
    totalTimeForApplication = sorted(totalTimeForApplication.items(), key=lambda x: x[1]["Usage time"],
                                     reverse=True)  # sorting dictionary in descending order
    # timeTotal = time.strftime('%Hh %Mm %Ss', time.gmtime(timeTotal))      może zmienić w format czasu w liście a może nie
    print(totalTimeForApplication)
    print('=' * 50)
    return totalTimeForApplication


def defSortingInstances(jsonData):
    for keyNumber in range(len(jsonData)):
        applicationKey = list(jsonData.keys())
        jsonData[applicationKey[keyNumber]] = sorted(jsonData[applicationKey[keyNumber]], key=lambda x: x["total"],reverse=True)
    print(jsonData)
    return jsonData

def defPrintingInstances(jsonData, instanceName):
    for instance in range(len(jsonData[instanceName])):
        print(jsonData[instanceName][instance])

data = defLoadDate()
totalUsageTimeForApplication = defSummingUpTotalTime(jsonData=data)
data = defSortingInstances(data)
instance = ''
instance = input("Please give the name of application ")
defPrintingInstances(data, instanceName=instance)
defIterateJson(data)
