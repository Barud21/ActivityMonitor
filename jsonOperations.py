import json
import time
from operator import itemgetter, attrgetter

# loads json data to memory
def defLoadDate(file_name):
    with open(file_name, 'r') as read_date:
        dateData = json.load(read_date)
    return dateData

# iterates through whole json file
def defIterateJson(jsonData):
    for instance in range(len(jsonData)):                   # loop through every major object in list
        print(json.dumps(jsonData[instance], indent=4))     # printing up the data from json
        print('=' * 50)
    return

# function that sums up total usage time for every application, creates dictionary, where applications are keys and total time is a value,
# then it sorts the list in descending order
def defSummingUpTotalTime(jsonData):
    totalTimeForApplication = {}
    for dataNumber in range(len(jsonData)):                                                                     # iterating through major applications
        timeTotal = 0                                                                                           # defining total time variable
        applicationKey = list(jsonData[dataNumber].keys())                                                      # finding key (application name), which is different for every object
        for instance in range(len(jsonData[dataNumber][applicationKey[0]]["instances"])):                       # iterating through instances in every application
            timeTotal += jsonData[dataNumber][applicationKey[0]]["instances"][instance]["total"]                # summimg up time from every instance
        print("Total time value for {0} instance is {1}".format(dataNumber, timeTotal))
        totalTimeForApplication[applicationKey[0]] = timeTotal                                                  # creating dictionary, where applications are keys and values are total usage times
    totalSortedTimeForApplications = sorted(totalTimeForApplication.items(), key=itemgetter(1), reverse=True)   # sorting dictionary in descending order
    print(totalTimeForApplication)
    print(totalSortedTimeForApplications)
    return totalTimeForApplication


def defSortingInstances(jsonData):
    sortedData = jsonData

    for dataNumber in range(len(jsonData)):
        applicationKey = list(jsonData[dataNumber].keys())
        sortedData[dataNumber][applicationKey[0]]["instances"] = sorted(jsonData[dataNumber][applicationKey[0]]["instances"], key=lambda x: x["total"],reverse=True)

    #sortedData[0]["Opera"]["instances"] = sorted(jsonData[0]["Opera"]["instances"], key=lambda x : x["total"], reverse = True)
    print(sortedData)
    print(jsonData[0])
    #sortedJson["total"]
    return sortedData

data = defLoadDate(file_name="2020_02_05.json")
print(len(data[0]["Opera"]["instances"]))
print(data[0]["Opera"])
print(json.dumps(data, indent=4))
print()
print(data[0]["Opera"]["instances"][0]["total"])
#defSummingUpTotalTime(data)
totalUsaegTimeForApplication = defSummingUpTotalTime(jsonData=data)
data = defSortingInstances(data)
#totalUsaegTimeForApplication = {}

print(data)
print(totalUsaegTimeForApplication)
#defIterateJson(jsonData=data)