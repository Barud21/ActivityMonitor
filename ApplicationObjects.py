from dataclasses import dataclass
from typing import List
import datetime

@dataclass
class TimeStamp:
    start: datetime.time
    end: datetime.time

    def calculateTimeDiffInSecs(self):
        placeholder_date = datetime.datetime(datetime.MINYEAR, 1, 1)
        new_start_datetime = datetime.datetime.combine(placeholder_date, self.start)
        new_end_datetime = datetime.datetime.combine(placeholder_date, self.end)

        return int((new_end_datetime - new_start_datetime).total_seconds())


@dataclass
class DetailedInstance:
    detailedName: str
    timestamps: List[TimeStamp]
    totalTime: int = 0  # in seconds

    def __post_init__(self):
        for ts in self.timestamps:
            self.totalTime += ts.calculateTimeDiffInSecs()

    def addTimeStamp(self, ts: TimeStamp):
        if ts not in self.timestamps:
            self.timestamps.append(ts)
            self.totalTime += ts.calculateTimeDiffInSecs()


@dataclass
class ApplicationWithInstances:
    appName: str
    instances: List[DetailedInstance]

    def updateOrAddInstance(self, di: DetailedInstance):
        instanceDetailedNames = [x.detailedName for x in self.instances]

        if di.detailedName not in instanceDetailedNames:
            self.instances.append(di)
        else:
            for instance in self.instances:
                if di.detailedName == instance.detailedName:
                    for ts in di.timestamps:
                        instance.addTimeStamp(ts)
                    break

    #gets instances from another instance and based on them update this instance
    def updateBasedOnOther(self, other):
        if self.appName == other.appName:
            for i in other.instances:
                self.updateOrAddInstance(i)

    def sumOfTotalTimeForApplication(self):
        totalTimeForApp = 0
        for instance in self.instances:
            totalTimeForApp += instance.totalTime
        return totalTimeForApp
