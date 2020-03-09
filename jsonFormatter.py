import ApplicationObjects as Ao
import json
import time
import datetime


#TODO: Make naming of all fields consistent; camelCase?
#Allows to specify how object of our custom classes should be represented as json
class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Ao.TimeStamp):
            return{
                #split to remove the micrseconds part, they are after the only coma in the string representation
                #without split it looks like: 20:11:48.098846
                "start": str(obj.start.time()).split('.')[0],
                "end": str(obj.end.time()).split('.')[0]
            }
        elif isinstance(obj, Ao.DetailedInstance):
            return {
                "detailed_name": obj.detailedName,
                "timestamps": obj.timestamps,
                #TODO:Change to totalTime, so .json file will be self explanatory
                "total": obj.totalTime
            }
        elif isinstance(obj, Ao.ApplicationWithInstances):
            return {
                'appName': obj.appName,
                'instances': obj.instances
            }
        # to raise the TypeError when needed
        return super(CustomJsonEncoder, self).default(obj)


#Allows to specify the rules based on which we are deserializing the json into objects of our custom classes
class CustomJsonDecoder(json.JSONDecoder):
    #lists with keys, that will be present when our object is __dict__'ed; used for easier object checks in deserialization
    #must map list of keys present in the json file
    timestampElements = ['start', 'end']
    detailedInstanceElements = ['detailed_name', 'timestamps', 'total']
    applicationElements = ['appName', 'instances']

    def __init__(self, *args, **kwargs):
        self.timestampElements.sort()
        self.detailedInstanceElements.sort()
        self.applicationElements.sort()

        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        detected_keys = list(obj.keys())
        detected_keys.sort()

        if detected_keys == self.timestampElements:
            #TODO: Take care of datetime.now(); this can be a mess when we load files from previous days; but on the other hand it may actually work well if all dates in one file will be set as the same day.
            year = datetime.datetime.now().year
            month = datetime.datetime.now().month
            day = datetime.datetime.now().day
            startHours, startMinutes, startSeconds = obj['start'].split(':')
            endHours, endMinutes, endSeconds = obj['end'].split(':')

            startTime = datetime.datetime(year, month, day, int(startHours), int(startMinutes), int(startSeconds))
            endTime = datetime.datetime(year, month, day, int(endHours), int(endMinutes), int(endSeconds))
            return Ao.TimeStamp(startTime, endTime)

        elif detected_keys == self.detailedInstanceElements:
            detailed_name = obj['detailed_name']
            detailed = Ao.DetailedInstance(detailed_name, [])
            for ts in obj['timestamps']:
                detailed.addTimeStamp(ts)
            return detailed

        elif detected_keys == self.applicationElements:
            applicationName = obj['appName']
            entireApp = Ao.ApplicationWithInstances(applicationName, [])
            for di in obj['instances']:
                entireApp.updateOrAddInstance(di)
            return entireApp

        else:
            return obj


#just for testing new things and playing around
if __name__ == '__main__':
    start = datetime.datetime.now()
    time.sleep(2)
    end = datetime.datetime.now()

    start2 = datetime.datetime.now()
    time.sleep(2)
    end2 = datetime.datetime.now()

    a = Ao.TimeStamp(start, end)
    b = Ao.TimeStamp(start2, end2)

    detailed_1 = Ao.DetailedInstance('youtube.com', [])
    detailed_1.addTimeStamp(a)
    detailed_1.addTimeStamp(b)

    detailed_2 = Ao.DetailedInstance('9gag.com', [])
    detailed_2.addTimeStamp(a)

    entireApp = Ao.ApplicationWithInstances('Opera', [])
    entireApp.updateOrAddInstance(detailed_1)
    entireApp.updateOrAddInstance(detailed_2)


    detailed_3 = Ao.DetailedInstance('MyNovelFinalEditLast7.docx', [])
    detailed_3.addTimeStamp(a)

    entireApp2 = Ao.ApplicationWithInstances('Word', [])
    entireApp2.updateOrAddInstance(detailed_3)

    AppsList = [entireApp, entireApp2]
    print(AppsList)
    encodedTs = json.dumps(AppsList, cls=CustomJsonEncoder)
    print(encodedTs)
    decoded = json.loads(encodedTs, cls=CustomJsonDecoder)
    print('Decoded', decoded)


