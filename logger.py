import win32gui, win32process
import psutil

import datetime
import time

from InternetBrowserHandler import InternetBrowserHandler
import ApplicationObjects as Ao


class Logger:
    def __init__(self):
        self.scanning_interval = 5  # seconds
        self.InternetBrowser = InternetBrowserHandler()
        self.applications = []

    #gets process name for a given windows handle
    def __getAppNameFromHndl (self, win_hndl):
        pid = win32process.GetWindowThreadProcessId(win_hndl)

        try:
            appName = psutil.Process(pid[-1]).name()
        except psutil.NoSuchProcess:
            appName = ''
        return appName

    #returns both app name and url
    def __getCurrentAppNameAndPossibleUrl (self, win_hndl):
        appName = self.__getAppNameFromHndl(win_hndl)
        appName = appName.lower().replace('.exe', '')
        url = self.InternetBrowser.connectToHndlFetchPossibleUrl(win_hndl)

        return appName, url

    #space saving method, for easier creation of DetailedInstance object
    def __createTempDetailedInstance(self, windowName, url, startTime, endTime):
        timestamp = Ao.TimeStamp(startTime, endTime)
        if url != '':
            detailedName = url
        else:
            detailedName = windowName
        return Ao.DetailedInstance(detailedName, [timestamp])

    #adds a new application if not logged before or updates the existing one
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


    #main loop, that will periodically scan for an application change and update objects on internal list of applications
    def scan(self):
        prev_text, prevAppName, prevUrl = '', '', ''
        beginning_time = datetime.datetime.now()

        while True:
            win_hndl = win32gui.GetForegroundWindow()
            current_text = win32gui.GetWindowText(win_hndl)

            if current_text != prev_text:
                currentAppName, currentUrl = self.__getCurrentAppNameAndPossibleUrl(win_hndl)
                # (application changed) OR (the same app but different url) OR (the same app but different window name and no url found)
                if (prevAppName != currentAppName) or \
                        ((prevAppName == currentAppName) and
                         ((prevUrl != currentUrl) or (currentUrl == prevUrl == '' and prev_text != current_text))):
                    ending_time = datetime.datetime.now()
                    print(prev_text,
                          prevAppName,
                          prevUrl,
                          beginning_time.time(),
                          ending_time.time(),
                          (ending_time - beginning_time).total_seconds()
                          )
                    self.__updateApplicationsList(prev_text, prevAppName, prevUrl, beginning_time.time(), ending_time.time())

                    beginning_time = datetime.datetime.now()

            #TODO: Maybe should be moved to if? Potential problem when currentAppName is not assigned yet
            prevAppName = currentAppName
            prevUrl = currentUrl
            prev_text = current_text

            time.sleep(self.scanning_interval)


if __name__ == '__main__':
    littleLoggyOne = Logger()
    littleLoggyOne.scan()






