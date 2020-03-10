from dataclasses import dataclass
from typing import List
import time #just for test
import datetime

@dataclass
class TimeStamp:
    start: datetime.datetime
    end: datetime.datetime

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.start == other.start and self.end == other.end
        return False

    def calculateTimeDiffInSecs(self):
        return int((self.end - self.start).total_seconds())


@dataclass
class DetailedInstance:
    detailedName: str
    timestamps: List[TimeStamp]
    totalTime: int = 0

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

    def getFirstTimeStamp(self):
        return self.timestamps[0]


@dataclass
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
                if instance == di:
                    instance.addTimeStamp(di.getFirstTimeStamp())


#just for testing new things and playing around
if __name__ == '__main__':

    start = datetime.datetime.now()
    time.sleep(2)
    end = datetime.datetime.now()

    a = TimeStamp(start, end)
    print(a.calculateTimeDiffInSecs())

    detailed = DetailedInstance('9gag.com', [a])

    entireApp = ApplicationWithInstances('Opera', [detailed])

    start = datetime.datetime.now()
    time.sleep(2)
    end = datetime.datetime.now()
    b = TimeStamp(start, end)

    detailed2 = DetailedInstance('youtube.com', [a, b])

    entireApp.updateOrAddInstance(detailed2)