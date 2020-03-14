from dataclasses import dataclass
from typing import List
import time #just for test
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
    totalTime: int = 0  #in seconds

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


#just for testing new things and playing around
if __name__ == '__main__':

    start = datetime.datetime.now().time()
    time.sleep(2)
    end = datetime.datetime.now().time()

    a = TimeStamp(start, end)
    detailed = DetailedInstance('9gag.com', [a])

    entireApp = ApplicationWithInstances('Opera', [detailed])


    start = datetime.datetime.now().time()
    time.sleep(2)
    end = datetime.datetime.now().time()
    b = TimeStamp(start, end)

    detailed2 = DetailedInstance('youtube.com', [a, b])

    entireApp.updateOrAddInstance(detailed2)

    start = datetime.datetime.now().time()
    time.sleep(2)
    end = datetime.datetime.now().time()
    c = TimeStamp(start, end)
    detailed3 = DetailedInstance('9gag.com', [c])

    entireApp.updateOrAddInstance(detailed3)
    print(entireApp)