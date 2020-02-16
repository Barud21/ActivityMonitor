from pywinauto import Application
import re


class InternetBrowserHandler:

    def __findPotentialUrlsFromBrowser (self, dialog):
        # fetched_url = dlg.child_window(title="Pole adresu", control_type="Edit").get_value()
        # below is a workaround to avoid language specific names
        potential_urls = []
        for d in dialog.descendants():
            control_type = d._BaseWrapper__repr_texts()[2]
            if control_type == 'Edit':  # in one of these fields, url is hidden (tested only for chromium)
                control_name = d._BaseWrapper__repr_texts()[1]
                potential_urls.append(dialog.child_window(title=control_name, control_type="Edit").get_value())

        return potential_urls

    def __findUrlInStringList (self,potential_urls):
        urlFound = False
        for maybeUrl in potential_urls:
            result_tuple = self.__isStringAnUrl(maybeUrl)
            if result_tuple[0]:
                found_url = result_tuple[1]
                urlFound = True
                break
        if not urlFound:
            found_url = ''

        return found_url

    # checks if given string is an url;
    # returns tuple: ({logic value if string is an url}, {domain name if string is an url, empty string otherwise})
    def __isStringAnUrl(self, string_to_check):
        regExForAWebsite = re.compile(r"""^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?
           ([a-z0-9]+
           ([\.][a-z0-9]+)*
           \.[a-z]{2,5})
           (:[0-9]{1,5})?
           (\/.*)?$""", re.IGNORECASE | re.VERBOSE)
        mo = regExForAWebsite.search(string_to_check)
        if mo is None:
            return (False, '')
        else:
            return (True, mo.group(2))


    def connectToHndlFetchPossibleUrl(self, win_hndl):
        app = Application(backend='uia')

        try:
            app.connect(handle=win_hndl)
            dlg = app.top_window()
        except RuntimeError:
            print('Couldnt connect to last application :(')
            fetched_url = ''
        else:
            try:
                potential_urls = self.__findPotentialUrlsFromBrowser(dlg)
            except:
                fetched_url = ''
            else:
                fetched_url = self.__findUrlInStringList(potential_urls)

        return fetched_url