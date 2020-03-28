import ApplicationObjects as Ao
import json
import datetime


# Allows to specify how object of our custom classes should be represented as json
class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Ao.TimeStamp):
            return{
                # split to remove the microseconds part, they are after the only coma in the string representation
                # without split it looks like: 20:11:48.098846
                "start": str(obj.start).split('.')[0],
                "end": str(obj.end).split('.')[0]
            }
        elif isinstance(obj, Ao.DetailedInstance):
            return {
                "detailedName": obj.detailedName,
                "timestamps": obj.timestamps,
                "totalTime": obj.totalTime
            }
        elif isinstance(obj, Ao.ApplicationWithInstances):
            return {
                'appName': obj.appName,
                'instances': obj.instances
            }
        # to raise the TypeError when needed
        return json.JSONEncoder.default(obj)


# Allows to specify the rules based on which we are deserializing the json into objects of our custom classes
class CustomJsonDecoder(json.JSONDecoder):
    # lists with keys, that will be present when our object is __dict__'ed; used for easier object checks in deserialization
    # must map list of keys present in the json file
    timestampElements = ['start', 'end']
    detailedInstanceElements = ['detailedName', 'timestamps', 'totalTime']
    applicationElements = ['appName', 'instances']

    def __init__(self, *args, **kwargs):
        self.timestampElements.sort()
        self.detailedInstanceElements.sort()
        self.applicationElements.sort()

        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        detected_keys = list(obj.keys())
        detected_keys.sort()

        # deserializing based on the keys in the dict.
        # If we found a dict, that has the keys as in our template list, then create object of given class
        if detected_keys == self.timestampElements:
            startHours, startMinutes, startSeconds = obj['start'].split(':')
            endHours, endMinutes, endSeconds = obj['end'].split(':')

            startTime = datetime.time(int(startHours), int(startMinutes), int(startSeconds))
            endTime = datetime.time(int(endHours), int(endMinutes), int(endSeconds))
            return Ao.TimeStamp(startTime, endTime)

        elif detected_keys == self.detailedInstanceElements:
            detailed_name = obj['detailedName']
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
