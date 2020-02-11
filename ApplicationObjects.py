from dataclasses import dataclass
from typing import List
import time #just for test
import datetime


@dataclass
class TimeStamp:
    start: datetime.datetime
    end: datetime.datetime

    def calculateTimeDiffInSecs(self):
        return (end - start).total_seconds()


@dataclass
class DetailedInstance:
    detailedName: str
    timestamps: List[TimeStamp]
    totalTime: int = 0

    def addTimeStamp(self, ts: TimeStamp):
        if not ts in self.timestamps:
            self.timestamps.append(ts)
            self.totalTime += ts.calculateTimeDiffInSecs()


@dataclass
class ApplicationWithInstances:
    name: str
    instances: List[DetailedInstance]


if __name__ == '__main__':

    start = datetime.datetime.now()
    time.sleep(2)
    end = datetime.datetime.now()

    a = TimeStamp(start, end)
    print(a.calculateTimeDiffInSecs())
    # b = TimeStamp(start=datetime.datetime.now().time().__str__(), end=datetime.datetime.now().time().__str__())
    #
    detailed = DetailedInstance('9gag.com', [a])
    print(detailed)

    start = datetime.datetime.now()
    time.sleep(2)
    end = datetime.datetime.now()

    b = TimeStamp(start, end)
    detailed.addTimeStamp(b)
    print(detailed)
