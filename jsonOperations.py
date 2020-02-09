import json
from _datetime import datetime
from operator import itemgetter


# loads json data to memory
def defLoadDate():
    fileName = datetime.today().strftime('%Y_%m_%d') + ".json"          # opening file with today's date by default
    with open(fileName, 'r') as read_date:                              # opening file with today's date
        dateData = json.load(read_date)                                 # loading data to memory
    return dateData                                                     # returning data


# iterates through whole json file
def defIterateJson(jsonData):
    for instance in range(len(jsonData)):                               # loop through every major object in list
        print(json.dumps(jsonData[instance], indent=4))                 # printing up the data from json
        print('=' * 50)
    return


# function that sums up total usage time for every application, creates dictionary, where applications are keys
# and total time is a value, then it sorts the list in descending order
def defSummingUpTotalTime(jsonData):
    totalTimeForApplication = {}
    for dataNumber in range(len(jsonData)):                                                                     # iterating through major applications
        timeTotal = 0                                                                                           # defining total time variable
        applicationKey = list(jsonData[dataNumber].keys())                                                      # finding key (application name), which is different for every object
        for instance in range(len(jsonData[dataNumber][applicationKey[0]]["instances"])):                       # iterating through instances in every application
            timeTotal += jsonData[dataNumber][applicationKey[0]]["instances"][instance]["total"]                # summimg up time from every instance
        print("Total time value for {0} instance is {1}".format(dataNumber, timeTotal))
        totalTimeForApplication[applicationKey[0]] = timeTotal                                                  # creating dictionary, where applications are keys and values are total usage times
    totalTimeForApplication = sorted(totalTimeForApplication.items(), key=itemgetter(1), reverse=True)          # sorting dictionary in descending order
    print(totalTimeForApplication)
    return totalTimeForApplication


def defSortingInstances(jsonData):
    for dataNumber in range(len(jsonData)):
        applicationKey = list(jsonData[dataNumber].keys())
        jsonData[dataNumber][applicationKey[0]]["instances"] = \
            sorted(jsonData[dataNumber][applicationKey[0]]["instances"], key=lambda x: x["total"],reverse=True)
    print(jsonData)
    return jsonData


data = defLoadDate()
totalUsageTimeForApplication = defSummingUpTotalTime(jsonData=data)
data = defSortingInstances(data)

$ pip freeze > requirements_br.txt