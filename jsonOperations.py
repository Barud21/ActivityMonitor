import json
import time

def defLoadDate(file_name):
    with open(file_name, 'r') as read_date:
        dateData = json.load(read_date)
    return dateData


def defIterateJson(jsonData):
    for instance in range(len(jsonData)):
        print(json.dumps(jsonData[instance], indent=4))
        print('=' * 50)
    return


def defSummingUpTotalTime(jsonData):
    for data_length in range(len(jsonData)):
        timeTotal = 0
        key = list(jsonData[data_length].keys())
        for instance in range(len(jsonData[data_length][key[0]]["instances"])):
            timeTotal += jsonData[data_length][key[0]]["instances"][instance]["total"]
        print("Total time value for {0} instance is {1}".format(data_length, timeTotal))
    return


def defSortingInstances(jsonData):
    sortedData = jsonData
    sortedData[0]["Opera"]["instances"] = sorted(jsonData[0]["Opera"]["instances"], key=lambda x : x["total"], reverse = True)
    print(sortedData)
    print(jsonData[0])
    #sortedJson["total"]
    return

data = defLoadDate(file_name="file_exem.json")
print(len(data[0]["Opera"]["instances"]))
print(data[0]["Opera"])
print(json.dumps(data, indent=4))
print()
print(data[0]["Opera"]["instances"][0]["total"])
defSummingUpTotalTime(data)
defSortingInstances(data)
#defIterateJson(jsonData=data)