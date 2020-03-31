import datetime
import os

import ApplicationObjects as Ao


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


def getAbsPath(filename, fileAtr):
    dirAbsPath = os.path.dirname(os.path.abspath(fileAtr))
    return os.path.join(dirAbsPath, filename)


def getResultFromFile(fileRelativePath, fileAtr):
    with open(getAbsPath(fileRelativePath, fileAtr)) as result_file:
        return result_file.read()


def removeWhitespacesFromString(s):
    return ''.join(s.split())
