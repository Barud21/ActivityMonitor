import datetime
import json
import os

import ApplicationObjects as Ao
import jsonFormatter as jF

def createTimestamp(timeDigitsTup):
    t1 = datetime.time(timeDigitsTup[0][0], timeDigitsTup[0][1], timeDigitsTup[0][2])
    t2 = datetime.time(timeDigitsTup[1][0], timeDigitsTup[1][1], timeDigitsTup[1][2])
    return Ao.TimeStamp(t1, t2)


def createDetailedInstance(timeDigitsTupList, instanceName):
    timestamps = []
    for tdt in timeDigitsTupList:
        timestamps.append(createTimestamp(tdt))

    return Ao.DetailedInstance(instanceName, timestamps)


def createBasicApp(timeDigitsTupList, instanceName, appName):
    detailed = createDetailedInstance(timeDigitsTupList, instanceName)
    return Ao.ApplicationWithInstances(appName, [detailed])


# fileAtr here so we can build an absolute path based on the file when call this function
# so we can specifiy paths in test file, relatively to the test file itself, for a better readability
def getAbsPath(filename, fileAtr):
    dirAbsPath = os.path.dirname(os.path.abspath(fileAtr))
    return os.path.join(dirAbsPath, filename)


def getResultFromFileInString(fileRelativePath, fileAtr):
    with open(getAbsPath(fileRelativePath, fileAtr), encoding='utf8') as result_file:
        return result_file.read()


def getJsonObjectsFromFile(filePath, fileAtr):
    with open(getAbsPath(filePath, fileAtr), 'r',  encoding='utf8') as input_file:
        return json.load(input_file, cls=jF.CustomJsonDecoder)


def dumpObjectsToJsonString(objects):
    return json.dumps(objects, cls=jF.CustomJsonEncoder, ensure_ascii=False)


def removeWhitespacesFromString(s):
    return ''.join(s.split())
