import win32gui, win32process
import psutil
import datetime
import time
import os
import json
import logging

from InternetBrowserHandler import InternetBrowserHandler
import ApplicationObjects as Ao
import jsonFormatter


class Logger:
    def __init__(self):
        self.scanningInterval = 30  # seconds
        self.fileWritingInterval = 300  # seconds
        self.filesDirName = 'GeneratedFiles'
        self.InternetBrowser = InternetBrowserHandler()
        self.applications = []

        if not os.path.isdir(self.filesDirName):
            os.mkdir(self.filesDirName)

        logging.basicConfig(filename='app.log', format='%(asctime)s - %(levelname)s - %(message)s')

    # gets process name for a given windows handle
    def __getAppNameFromHndl (self, win_hndl):
        pid = win32process.GetWindowThreadProcessId(win_hndl)

        try:
            appName = psutil.Process(pid[-1]).name()
        except psutil.NoSuchProcess:
            appName = ''
        return appName

    # returns both app name and url
    def __getCurrentAppNameAndPossibleUrl (self, win_hndl):
        appName = self.__getAppNameFromHndl(win_hndl)
        appName = appName.lower().replace('.exe', '')
        url = self.InternetBrowser.connectToHndlFetchPossibleUrl(win_hndl)

        return appName, url

    # space saving method, for easier creation of DetailedInstance object
    def __createTempDetailedInstance(self, windowName, url, startTime, endTime):
        timestamp = Ao.TimeStamp(startTime, endTime)
        if url != '':
            detailedName = url
        else:
            detailedName = windowName
        return Ao.DetailedInstance(detailedName, [timestamp])

    # adds a new application if not logged before or updates the existing one
    def __updateApplicationsList(self, windowName, appName, url, startTime, endTime):

        detailedInst = self.__createTempDetailedInstance(windowName, url, startTime, endTime)

        appNames = [x.appName for x in self.applications]
        if appName not in appNames:
            self.applications.append(Ao.ApplicationWithInstances(appName, [detailedInst]))
        else:
            for application in self.applications:
                if appName == application.appName:
                    application.updateOrAddInstance(detailedInst)
                    break

     # takes other application list and extends it (only addition is done) based on the self.applications
    def __updateOtherAplicationsList(self, other):
        for loggedApp in self.applications:
            if loggedApp.appName not in [x.appName for x in other]:         #add new ApplicationWithInstances
                other.append(loggedApp)
            else:         #update already existing ones
                for nd_app in other:
                    if nd_app.appName == loggedApp.appName:
                        nd_app.updateBasedOnOther(loggedApp)

    # TODO: Make it async (threading) - what about exceptions in thread? Shared self.applications between the threads?
    def _updateFile(self):
        file_name = datetime.datetime.today().strftime('%Y_%m_%d') + ".json"
        file_path = os.path.join(self.filesDirName, file_name)
        print('File update in ', file_path)

        # open file and read data from it
        try:
            with open(file_path, 'r', encoding='utf8') as file:
                loaded_raw_text = file.read()
                file.seek(0)
                loaded_data = json.load(file, cls=jsonFormatter.CustomJsonDecoder)
        except FileNotFoundError:
            with open(file_path, 'w') as file:
                pass    # just create an empty file
            loaded_data = []
        except json.decoder.JSONDecodeError:
            if loaded_raw_text:
                logging.exception('File is corrupted, exiting ;(')
                # exit()
                raise
            else:
                loaded_data = []

        # create new application list, update loaded data with self.applications
        new_data = loaded_data
        self.__updateOtherAplicationsList(new_data)

        # serialize new list to json string
        json_new_data = json.dumps(new_data, cls=jsonFormatter.CustomJsonEncoder, ensure_ascii=False)

        # save new data to file
        with open(file_path, 'w', encoding='utf8') as file:
            file.write(json_new_data)

        # clear self.applications, we dont want to store things we already wrote to file
        self.applications.clear()

    # main loop, that will periodically scan for an application change and update objects on internal list of applications
    def scan(self):
        prev_text, prevAppName, prevUrl = '', '', ''
        beginning_time = datetime.datetime.now()
        writingTimePoint = datetime.datetime.now()

        while True:
            win_hndl = win32gui.GetForegroundWindow()
            current_text = win32gui.GetWindowText(win_hndl)

            shouldWriteNowBecauseOfDayChanging = False
            thisPointOfDateTime = datetime.datetime.now()
            if (thisPointOfDateTime + datetime.timedelta(seconds=self.scanningInterval)).day != thisPointOfDateTime.day:
                shouldWriteNowBecauseOfDayChanging = True

            if shouldWriteNowBecauseOfDayChanging:
                ending_time = datetime.datetime(thisPointOfDateTime.year, thisPointOfDateTime.month, thisPointOfDateTime.day, 23, 59, 59)
                self.__updateApplicationsList(prev_text, prevAppName, prevUrl, beginning_time.time(),
                                              ending_time.time())
                print(prev_text,
                      prevAppName,
                      prevUrl,
                      beginning_time.time(),
                      ending_time.time(),
                      (ending_time - beginning_time).total_seconds()
                      )
                beginning_time = ending_time + datetime.timedelta(seconds=1)
                self._updateFile()

            if current_text != prev_text:
                currentAppName, currentUrl = self.__getCurrentAppNameAndPossibleUrl(win_hndl)
                # (application changed) OR (the same app but different url) OR (the same app but different window name and no url found)
                # check for prev_text and prevAppName != '' to prevent from the first empty entry which was always added on startup
                if ((prevAppName != currentAppName) or
                        ((prevAppName == currentAppName) and
                         ((prevUrl != currentUrl) or (currentUrl == prevUrl == '' and prev_text != current_text))))\
                        and (prev_text != '' and prevAppName != ''):
                    ending_time = datetime.datetime.now()
                    print(prev_text,
                          prevAppName,
                          prevUrl,
                          beginning_time.time(),
                          ending_time.time(),
                          (ending_time - beginning_time).total_seconds()
                          )
                    self.__updateApplicationsList(prev_text, prevAppName, prevUrl, beginning_time.time(),
                                                  ending_time.time())

                    beginning_time = datetime.datetime.now()

                prevAppName = currentAppName
                prevUrl = currentUrl
                prev_text = current_text

            if (datetime.datetime.now() - writingTimePoint).total_seconds() > self.fileWritingInterval:
                if len(self.applications) > 0:
                    self._updateFile()
                writingTimePoint = datetime.datetime.now()

            time.sleep(self.scanningInterval)


if __name__ == '__main__':
    littleLoggyOne = Logger()

    try:
        littleLoggyOne.scan()
    except Exception as e:
        logging.exception(f'Exception occurred. Dump of currently stored applications list which was not saved to file yet: {littleLoggyOne.applications}')
        raise

# TODO: Support for windows signals, to not break when system goes to sleep/hybernate. Ideally, write what you already logged, and start working again after is all back again
# ^ Works well if sleep time is relatively small (like 5mins), when it was around 40 mins it stopped working (needs more investigation)
# TODO: Support for having focus on windows desktop (for now we add this time to the previous application which is not right)
# ^ It seems that clicking on dektop manually works as expected, but using shortcut Win + D doesnt set focus on desktop by default, hence we log this time as the previously open application


