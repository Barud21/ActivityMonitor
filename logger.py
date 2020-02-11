import win32gui, win32process
import psutil

import datetime
import time


from InternetBrowserHandler import InternetBrowserHandler

class Logger:
    def __init__(self):
        self.scanning_interval = 5  # seconds
        self.InternetBrowser = InternetBrowserHandler()


    def __getAppNameFromHndl (self, win_hndl):
        pid = win32process.GetWindowThreadProcessId(win_hndl)

        try:
            appName = psutil.Process(pid[-1]).name()
        except psutil.NoSuchProcess:
            appName = ''
        return appName

    def __getCurrentAppNameAndPossibleUrl (self, win_hndl):
        appName = self.__getAppNameFromHndl(win_hndl)
        appName = appName.lower().replace('.exe', '')
        url = self.InternetBrowser.connectToHndlFetchPossibleUrl(win_hndl)

        return appName, url

    #main loop, that will periodically scan for a window name, if changed then fetch app name and potential url
    def scan(self):
        prev_text, prevAppName, prevUrl = '', '', ''
        begining_time = datetime.datetime.now()

        while True:
            win_hndl = win32gui.GetForegroundWindow()
            current_text = win32gui.GetWindowText(win_hndl)

            if current_text != prev_text:
                currentAppName, currentUrl = self.__getCurrentAppNameAndPossibleUrl(win_hndl)
                if (prevAppName != currentAppName) or (prevUrl != currentUrl):
                    endning_time = datetime.datetime.now()
                    print(prev_text, prevAppName, prevUrl, begining_time.time(), endning_time.time(), (endning_time - begining_time).total_seconds())

                    begining_time = datetime.datetime.now()


            prevAppName = currentAppName
            prevUrl = currentUrl
            prev_text = current_text

            time.sleep(self.scanning_interval)


if __name__ == '__main__':
    littleLoggyOne = Logger()
    littleLoggyOne.scan()






