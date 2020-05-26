import tkinter as tk
import matplotlib.figure
import matplotlib.patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import time
import jsonOperations as jO

window = tk.Tk()
window.minsize(900, 700)
window.title('Activity Monitor')

window.columnconfigure(0, weight=5000)
window.columnconfigure(1, weight=5000)
window.rowconfigure(0, weight=50)
window.rowconfigure(1, weight=5000)
window.rowconfigure(2, weight=5000)

# title frame declaration
titleFrame = Frame(window)
titleFrame.grid(row=0, column=0, columnspan=2, sticky='nsew')
titleFrame.config(border=10)
titleFrame.columnconfigure(0, weight=10)
titleFrame.rowconfigure(0, weight=10)
titleLabel = Label(titleFrame, text="Monitor aktywności - używasz na własną odpowiedzialność ;)")
titleLabel.grid(row=0, column=0, sticky='nsew')
titleLabel.config(font=14)

# pie chart frame declaration
pieFrame = Frame(window)
pieFrame.grid(row=1, column=0, rowspan=2, sticky='nsew')
pieFrame.config(border=5)
pieFrame.columnconfigure(0, weight=10)
pieFrame.columnconfigure(1, weight=10)
pieFrame.rowconfigure(0, weight=1)
pieFrame.rowconfigure(1, weight=10)

# applications frame declaration
appsFrame = Frame(window)
appsFrame.grid(row=1, column=1, sticky='nsew')
appsFrame.config(border=2)
appsFrame.columnconfigure(0, weight=10)
appsFrame.columnconfigure(1, weight=1)
appsFrame.rowconfigure(0, weight=10)
appsFrame.rowconfigure(1, weight=1)

# instances frame declaration
instancesFrame = Frame(window)
instancesFrame.grid(row=2, column=1, sticky='nsew')
instancesFrame.config(border=2)
instancesFrame.columnconfigure(0, weight=10)
instancesFrame.columnconfigure(1, weight=1)
instancesFrame.rowconfigure(0, weight=10)
instancesFrame.rowconfigure(1, weight=1)

# declaration of global variables
listOfFiles = jO.defListOfFiles()
latestFile = jO.defFindingLatestFile(listOfFiles)
data = jO.defDecodingJson(latestFile[1])
summedTime = jO.defSummingUpTotalTime(data)
percentageTime = jO.defPercentageCalculation(summedTime)
sortedInstances = jO.defSortedInstances(data)

# declaration of default data file
defaultFile = latestFile[0]
defaultDate = StringVar(pieFrame)
defaultDate.set(defaultFile)


# function, which updates applications and pie chart according to a choosen date
def DateSelect(value):
    for k in listOfFiles.keys():
        if k == value:
            applicationList.delete(0, 'end')
            instancesList.delete(0,'end')
            global data, summedTime, percentageTime, sortedInstances
            data = jO.defDecodingJson(listOfFiles[k])
            summedTime = jO.defSummingUpTotalTime(data)
            percentageTime = jO.defPercentageCalculation(summedTime)
            sortedInstances = jO.defSortedInstances(data)
            for zone in summedTime:
                applicationList.insert(tk.END, zone[0] + ' - ' + time.strftime('%H:%M:%S', time.gmtime(zone[1])))
            defDrawingPie(percentage=percentageTime, totalTime=summedTime)


# option menu for choosing date
datesMenuLabel = Label(pieFrame, text="Data:")
datesMenuLabel.grid(row=0, column=0, sticky='e')
datesMenu = tk.OptionMenu(pieFrame, defaultDate, *listOfFiles.keys(), command=DateSelect)
datesMenu.grid(row=0, column=1, sticky='w')


# drawing pie chart function
def defDrawingPie(percentage=percentageTime, totalTime=summedTime):
    fig = matplotlib.figure.Figure(figsize=(5,5))
    ax = fig.add_subplot(111)
    ax.pie(percentage, labels=[x[0] for x in totalTime], autopct='%1.1f%%', explode=[0.01 for x in totalTime])
    canvas = FigureCanvasTkAgg(fig, master=pieFrame)
    canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, sticky='nsew')
    canvas.draw()


defDrawingPie()

# instances list declaration
instancesList = tk.Listbox(instancesFrame)
instancesList.grid(row=0, column=0, sticky='nsew')
instancesList.config(border=2, relief='sunken')

instancesScrollVertical = tk.Scrollbar(instancesFrame, orient=tk.VERTICAL, command=instancesList.yview)
instancesScrollVertical.grid(row=0, column=1, sticky='nsw')
instancesList['yscrollcommand'] = instancesScrollVertical.set

instancesScrollHorizontal = tk.Scrollbar(instancesFrame, orient=tk.HORIZONTAL, command=instancesList.xview)
instancesScrollHorizontal.grid(row=1, column=0, sticky='sew')
instancesList['xscrollcommand'] = instancesScrollHorizontal.set


# function, which updates instances list according to choosen application
def AppSelect(evt):
    value = str((applicationList.get(applicationList.curselection())))
    value = value[:-11]

    for key in sortedInstances.keys():
        if key == value:
            instancesList.delete(0,'end')
            for x in range(len(sortedInstances[key])):
                instancesList.insert(tk.END, sortedInstances[key][x][0] + ' - ' + time.strftime('%H:%M:%S', time.gmtime(sortedInstances[key][x][1])))


# applications list declaration
applicationList = tk.Listbox(appsFrame)
applicationList.bind('<<ListboxSelect>>', AppSelect)
applicationList.grid(row=0, column=0, sticky='nsew')
applicationList.config(border=2, relief='sunken')
for zone in summedTime:
    applicationList.insert(tk.END, zone[0] + ' - ' + time.strftime('%H:%M:%S', time.gmtime(zone[1])))

applicationScrollVertical = tk.Scrollbar(appsFrame, orient=tk.VERTICAL, command=applicationList.yview)
applicationScrollVertical.grid(row=0, column=1, sticky='nsw')
applicationList['yscrollcommand'] = applicationScrollVertical.set

applicationScrollHorizontal = tk.Scrollbar(appsFrame, orient=tk.HORIZONTAL, command=applicationList.xview)
applicationScrollHorizontal.grid(row=1, column=0, sticky='sew')
applicationList['xscrollcommand'] = applicationScrollHorizontal.set

# main loop
window.mainloop()