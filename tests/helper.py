import datetime
import ApplicationObjects as Ao


def createTimestamp(timeDigitsTup):
    t1 = datetime.time(timeDigitsTup[0][0], timeDigitsTup[0][1], timeDigitsTup[0][2])
    t2 = datetime.time(timeDigitsTup[1][0], timeDigitsTup[1][1], timeDigitsTup[1][2])
    return Ao.TimeStamp(t1, t2)


def createBasicApp(timeDigitsTupList , InstanceName, AppName):
    timestamps = []
    for tdt in timeDigitsTupList:
        timestamps.append(createTimestamp(tdt))

    detailed = Ao.DetailedInstance(InstanceName, timestamps)
    return Ao.ApplicationWithInstances(AppName, [detailed])


def getResultFromFile(filePath):
    with open(filePath) as result_file:
        return result_file.read()


def removeWhitespacesFromString(s):
    return ''.join(s.split())
