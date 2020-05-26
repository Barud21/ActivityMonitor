# **Activity Monitor**  [![Python 3.7.4](https://img.shields.io/badge/python-3.7.4-yellow.svg)](https://www.python.org/)
## What it is?
It's a simple python application that allows you to track your activities on the computer.
It consists of 2 modules: 
* Logger - records how much time you spend on particular programs and writes it's output to the .json file. 
One file is stored locally for each day.
It detects a program change based on the window name/application name of the foreground window.
Additionally it tries to fetch a domain part of open url, based on the browser control elements - works well for chromium based browsers.
Minimal example of .json file:  
```json
[
    {
        "appName": "opera",
        "instances": [
            {
                "detailedName": "example.com",
                "timestamps": [
                    {
                        "start": "20:03:08",
                        "end": "20:03:18"
                    }
                ],
                "totalTime": 10
            }
        ]
    }
]
```  

* GUI - provides a way to visualize the text data using pie chart. Reads .json files generated by a logger module.

## Limitations
Windows only (Logger module bases on win32gui and pywinauto). Tested on Windows 10

## How to generate executable files?
We are using [PyInstaller](https://www.pyinstaller.org)  
Steps required to generate exec files:  
* Activate virtualenv
* pyinstaller.exe .\GUI.py --onefile --exclude-module=pytest -w  
* pyinstaller.exe .\logger.py --onefile --exclude-module=pytest -w  

Then logger.exe and GUI.exe files will be created in _dist_ directory.

## How to add a logger module to Windows autostart?
1. Create a shortcut to logger.exe
2. Open Autostart Windows directory:  
 2.1  Win + R  
 2.2 Type "shell:startup"
3. Put logger shortcut into Autostart Windows directory

## Known problems  
1. _Sometimes_ fetching an url of open website doesn't work correctly. In such case, name of the window is logged instead.
It is either related to browser magic or pywinauto module. I couldn't find a way to reproduce it on demand. Maybe You can help?  