import tkinter as tk
import matplotlib.figure
import matplotlib.patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import time
import jsonOperations as jO

window = tk.Tk()
window.minsize(600, 600)
window.title('Activity Monitor')

window.columnconfigure(0, weight=10000)
window.columnconfigure(1, weight=10000)
window.columnconfigure(2, weight=1)
window.columnconfigure(3, weight=10000)
window.columnconfigure(4, weight=1)
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1000000)
window.rowconfigure(2, weight=1)

# label = tk.Label(window, text = "Hello World")
# label.grid(row=0, column=0)

# TODO: Add element to choose a file
listOfFiles = jO.defListOfFiles()
latestFile = jO.defFindingLatestFile(listOfFiles)
data = jO.defDecodingJson(latestFile[1])
summedTime = jO.defSummingUpTotalTime(data)
percentageTime = jO.defPercentageCalculation(summedTime)
sortedInstances = jO.defSortedInstances(data)

default = latestFile[0]
defaultDate = StringVar(window)
defaultDate.set(default)


def DateSelect(value):
    #value = value.replace("/", "_")
    print(value)
    for k in listOfFiles.keys():
        if k == value:
            applicationList.delete(0, 'end')
            instancesList.delete(0,'end')
            data = jO.defDecodingJson(listOfFiles[k])
            summedTime = jO.defSummingUpTotalTime(data)
            percentageTime = jO.defPercentageCalculation(summedTime)
            sortedInstances = jO.defSortedInstances(data)
            for zone in summedTime:
                applicationList.insert(tk.END, zone[0] + ' - ' + time.strftime('%H:%M:%S', time.gmtime(zone[1])))


datesMenu = tk.OptionMenu(window, defaultDate, *listOfFiles.keys(), command=DateSelect)
datesMenu.grid(row=0, column=0)


fig = matplotlib.figure.Figure(figsize=(5,5))
ax = fig.add_subplot(111)
ax.pie(percentageTime)
ax.legend([x[0] for x in summedTime]) # summedTime[0][0]

canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().grid(row=1, column=0, sticky='nsew')
canvas.draw()

instancesList = tk.Listbox(window)
instancesList.grid(row=1, column=3, sticky='nsew')
instancesList.config(border=2, relief='sunken')


def AppSelect(evt):
    value = str((applicationList.get(applicationList.curselection())))
    value = value[:-11]

    for key in sortedInstances.keys():
        if key == value:
            instancesList.delete(0,'end')
            for x in range(len(sortedInstances[key])):
                instancesList.insert(tk.END, sortedInstances[key][x][0] + ' - ' + time.strftime('%H:%M:%S', time.gmtime(sortedInstances[key][x][1])))


applicationList = tk.Listbox(window)
applicationList.bind('<<ListboxSelect>>', AppSelect)
applicationList.grid(row=1, column=1, sticky='nsew')
applicationList.config(border=2, relief='sunken')
for zone in summedTime:
    applicationList.insert(tk.END, zone[0] + ' - ' + time.strftime('%H:%M:%S', time.gmtime(zone[1])))

applicationScrollVertical = tk.Scrollbar(window, orient=tk.VERTICAL, command=applicationList.yview)
applicationScrollVertical.grid(row=1, column=2, sticky='nsw')
applicationList['yscrollcommand'] = applicationScrollVertical.set

applicationScrollHorizontal = tk.Scrollbar(window, orient=tk.HORIZONTAL, command=applicationList.xview)
applicationScrollHorizontal.grid(row=2, column=1, sticky='sew')
applicationList['xscrollcommand'] = applicationScrollHorizontal.set

instancesScrollVertical = tk.Scrollbar(window, orient=tk.VERTICAL, command=instancesList.yview)
instancesScrollVertical.grid(row=1, column=4, sticky='nsw')
instancesList['yscrollcommand'] = instancesScrollVertical.set

instancesScrollHorizontal = tk.Scrollbar(window, orient=tk.HORIZONTAL, command=instancesList.xview)
instancesScrollHorizontal.grid(row=2, column=3, sticky='sew')
instancesList['xscrollcommand'] = instancesScrollHorizontal.set

window.mainloop()