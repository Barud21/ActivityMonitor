import json
import glob
import os
from _datetime import datetime
import jsonFormatter as jF


# TODO: unit test for that
def defDecodingJson(fileName = None):
    list_of_files = glob.glob('C:/Users/Bartek/Documents/_Projekty/Python/Pycharm_projects/ActivityMonitor/GeneratedFiles/*')

    if fileName == None:
         fileName = max(list_of_files, key=os.path.getctime)

    with open(fileName, 'r') as read_date:                              # opening the latest file in directory
        jsonData = json.load(read_date, cls=jF.CustomJsonDecoder)       # loading data to memory

    return jsonData, list_of_files


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
