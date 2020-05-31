import json
import glob
import os
import jsonFormatter as jF


def defListOfFiles():
    listOfFiles = glob.glob(os.path.join(os.getcwd(), 'GeneratedFiles\*'))
    dictOfFiles = {}

    for file in listOfFiles:
        key = file[-15:-5].replace("_", "/")
        dictOfFiles[key] = file

    return dictOfFiles


def defFindingLatestFile(dictionary):
    latestFile = list(dictionary.values())[-1]
    latestDate = list(dictionary.keys())[-1]

    return latestDate, latestFile


def defDecodingJson(fileName):
    with open(fileName, 'r', encoding='utf8') as read_date:                              # opening the latest file in directory
        jsonData = json.load(read_date, cls=jF.CustomJsonDecoder)       # loading data to memory

    return jsonData


# function that sums up total usage time for every applications and sorts application in descending order by total usage time
def defSummingUpTotalTime(applicationList):
    totalTimeForApplications = {}

    for application in applicationList:
        totalTimeForApplications[application.appName] = application.sumOfTotalTimeForApplication()

    totalTimeForApplications = sorted(totalTimeForApplications.items(), key=lambda x: x[1], reverse= True)
    return totalTimeForApplications


# function that calculates percentage time of usage for every application
def defPercentageCalculation(totalTimeForApplications):
    percentageUsage = []
    totalUsageTime = 0

    for app in totalTimeForApplications:
        totalUsageTime += app[1]

    for app in totalTimeForApplications:
        percentageUsage.append(round(app[1] / totalUsageTime * 100))

    return percentageUsage


def defSortedInstances(applicationList):
    sortedInstances = {}

    for application in applicationList:
        sortedInstances[application.appName] = {}
        for instance in range(len(application.instances)):
            sortedInstances[application.appName][application.instances[instance].detailedName] = application.instances[instance].totalTime
        sortedInstances[application.appName] = sorted(sortedInstances[application.appName].items(), key=lambda x: x[1], reverse=True)

    return sortedInstances
