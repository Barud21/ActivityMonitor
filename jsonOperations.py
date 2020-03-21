import json
from _datetime import datetime
import jsonFormatter as jF


def defDecodingJson():
    fileName = datetime.today().strftime('JSON_files/%Y_%m_%d') + ".json"

    with open(fileName, 'r') as read_date:                              # opening file with today's date
        jsonData = json.load(read_date, cls=jF.CustomJsonDecoder)       # loading data to memory
    print(jsonData)
    return jsonData


# function that sums up total usage time for every applications and sorts application in descending order by total usage time
def defSummingUpTotalTime(applicationList):
    totalTimeForApplications = {}

    for application in applicationList:
        totalTimeForApplications[application.appName] = application.sumOfTotalTimeForApplication()

    print(totalTimeForApplications)
    totalTimeForApplications = sorted(totalTimeForApplications.items(), key=lambda x: x[1], reverse= True)
    print(totalTimeForApplications)

    return totalTimeForApplications

# function that calculates percentage time of usage for every application
def defPercentageCalculation(totalTimeForApplications):
    percentageUsage = list()
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
        print(sortedInstances)

    print(sortedInstances)

    return sortedInstances

