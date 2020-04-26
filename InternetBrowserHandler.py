import re
import time

from pywinauto import Application



class InternetBrowserHandler:
    #iterate through all controls in the browser tab, url is in one of them, that has type = Edit
    def __findPotentialUrlsFromBrowser (self, dialogs):
        # fetched_url = dlg.child_window(title="Pole adresu", control_type="Edit").get_value()
        # below is a workaround to avoid language specific names
        potential_urls = []
        for dialog in dialogs:
            for d in dialog.descendants():
                control_type = d._BaseWrapper__repr_texts()[2]
                if control_type == 'Edit':  # in one of these fields, url is hidden (tested only for chromium)
                    control_text = d.get_value()
                    if control_text != '':
                        potential_urls.append(control_text)

        return potential_urls

    #goes through list of strings, if it finds that some string is an url then returns immediately; otherwise returns empty string
    def __findUrlInStringList (self, potential_urls):
        found_url = ''
        for maybeUrl in potential_urls:
            result_tuple = self.__isStringAnUrl(maybeUrl)
            if result_tuple[0]:
                found_url = result_tuple[1]
                break

        return found_url

    # checks if given string is an url;
    # returns tuple: ({logic value if string is an url}, {domain name if string is an url, empty string otherwise})
    def __isStringAnUrl(self, string_to_check):
        regExForAWebsite = re.compile(r"""^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?
           ([a-z0-9-_~]+
           ([\.][a-z0-9-_~]+)*
           \.[a-z]{2,5})
           (:[0-9]{1,5})?
           (\/.*)?$""", re.IGNORECASE | re.VERBOSE)
        mo = regExForAWebsite.search(string_to_check)
        if mo is None:
            return False, ''
        else:
            return True, mo.group(2)

    #connects to an application and tries to get an url of opened webpage if possible
    def connectToHndlFetchPossibleUrl(self, win_hndl):
        app = Application(backend='uia')

        try:
            app.connect(handle=win_hndl)
            dlgs = app.windows()    # for some reason when we fetch the list of opens windows for a given app, urls seems to be fetched always correctly, when we use app.top_window() sometimes url element is empty
                                    # when we handle list of windows; then top window is always first on the list; and during checking url validation whe always stop after getting the first url
                                    # hacky, but seems to work now
        except RuntimeError:
            print('Couldnt connect to last application :(')
            fetched_url = ''
        else:
            potential_urls = self.__findPotentialUrlsFromBrowser(dlgs)
            fetched_url = self.__findUrlInStringList(potential_urls)

            # XTODO: Think of a way to fix this brutal way; possibly dlg.wait() could be useful, need to play with it's
            # parameters, so this wait wouldnt fail
            # doesnt seem to necessary anymore
            # if fetched_url == '':
            #     time.sleep(1)
            #     potential_urls = self.__findPotentialUrlsFromBrowser(dlgs)
            #     fetched_url = self.__findUrlInStringList(potential_urls)

        return fetched_url
