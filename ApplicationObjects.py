from dataclasses import dataclass
from typing import List
import time #just for test
import datetime

@dataclass
class TimeStamp:
    start: datetime.time
    end: datetime.time

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.start == other.start and self.end == other.end
        return False

    def calculateTimeDiffInSecs(self):
        placeholder_date = datetime.datetime(datetime.MINYEAR, 1, 1)
        new_start_datetime = datetime.datetime.combine(placeholder_date, self.start)
        new_end_datetime = datetime.datetime.combine(placeholder_date, self.end)

        return int((new_end_datetime - new_start_datetime).total_seconds())


@dataclass
class DetailedInstance:
    detailedName: str
    timestamps: List[TimeStamp]
    totalTime: int = 0  #in seconds

    def __init__(self, detailedName, timestamps):
        self.detailedName = detailedName
        self.timestamps = []
        for ts in timestamps:
            self.addTimeStamp(ts)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.detailedName == other.detailedName

    def addTimeStamp(self, ts: TimeStamp):
        if ts not in self.timestamps:
            self.timestamps.append(ts)
            self.totalTime += ts.calculateTimeDiffInSecs()

    #TODO: do we really need this?
    def getFirstTimeStamp(self):
        return self.timestamps[0]


@dataclass
#TODO: add detailed instance through constructor
class ApplicationWithInstances:
    appName: str
    instances: List[DetailedInstance]

    #Do we really need this?
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.appName == other.appName

    def updateOrAddInstance(self, di: DetailedInstance):
        if di not in self.instances:
            self.instances.append(di)
        else:
            for instance in self.instances:
                if instance == di: #comparing them by names DetailedInstance.detailedName
                    instance.addTimeStamp(di.getFirstTimeStamp())


#just for testing new things and playing around
if __name__ == '__main__':

    start = datetime.datetime.now().time()
    time.sleep(2)
    end = datetime.datetime.now().time()

    a = TimeStamp(start, end)
    print(a.calculateTimeDiffInSecs())

    detailed = DetailedInstance('9gag.com', [a])

    entireApp = ApplicationWithInstances('Opera', [detailed])

    start = datetime.datetime.now().time()
    time.sleep(2)
    end = datetime.datetime.now().time()
    b = TimeStamp(start, end)

    detailed2 = DetailedInstance('youtube.com', [a, b])

    entireApp.updateOrAddInstance(detailed2)
