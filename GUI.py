import tkinter as tk
import matplotlib.figure
import matplotlib.patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import time
import jsonOperations as jO


class MainApplication:
    listOfFiles = jO.defListOfFiles()
    latestFile = jO.defFindingLatestFile(listOfFiles)
    data = jO.defDecodingJson(latestFile[1])
    summedTime = jO.defSummingUpTotalTime(data)
    percentageTime = jO.defPercentageCalculation(summedTime)
    sortedInstances = jO.defSortedInstances(data)
    selectedApp = None

    def __init__(self, master, *args, **kwargs):
        #tk.Frame.__init__(self, parent, *args, **kwargs)
        self.master = master

        master.title("Activity Monitor")
        master.minsize(1000, 800)
        master.columnconfigure(0, weight=5000)
        master.columnconfigure(1, weight=1000)
        master.rowconfigure(0, weight=50)
        master.rowconfigure(1, weight=5000)
        master.rowconfigure(2, weight=500)
        master.rowconfigure(3, weight=5000)

        self.titleFrame = Frame(master)
        self.pieFrame = Frame(master)
        self.appsFrame = LabelFrame(master, text="Application list", font=("Purisa", 11))
        self.applicationsList = tk.Listbox(self.appsFrame)
        self.instancesFrame = LabelFrame(master, text="Instance list", font=("Purisa", 11))

        self.defaultFile = self.latestFile[0]
        self.defaultDate = StringVar(self.pieFrame)
        self.defaultDate.set(self.defaultFile)

        self.titleFrameDeclaration()
        self.pieFrameDeclaration()
        self.appsFrameDeclaration()
        self.instancesFrameDeclaration()
        self.drawingPieChart()
        self.updateData()

    def titleFrameDeclaration(self):
        self.titleFrame.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self.titleFrame.config(border=10)
        self.titleFrame.columnconfigure(0, weight=10)
        self.titleFrame.rowconfigure(0, weight=10)
        self.titleLabel = Label(self.titleFrame, text="Activity Monitor - watch yourself!")
        self.titleLabel.grid(row=0, column=0, sticky='nsew')
        self.titleLabel.config(font=("Purisa", 14))

    def pieFrameDeclaration(self):
        self.pieFrame.grid(row=1, column=0, rowspan=3, sticky='nsew')
        self.pieFrame.config(border=5)
        self.pieFrame.columnconfigure(0, weight=10)
        self.pieFrame.columnconfigure(1, weight=10)
        self.pieFrame.rowconfigure(0, weight=1)
        self.pieFrame.rowconfigure(1, weight=10)

        self.datesMenuLabel = Label(self.pieFrame, text="Date: ")
        self.datesMenuLabel.grid(row=0, column=0, sticky='e')
        self.datesMenuLabel.config(font=("Purisa", 12))
        self.datesMenu = tk.OptionMenu(self.pieFrame, self.defaultDate, *self.listOfFiles.keys(), command=self.dateSelection)
        self.datesMenu.grid(row=0, column=1, sticky='w')
        self.datesMenu.config(font=("Purisa", 12))

    def appsFrameDeclaration(self):
        self.appsFrame.grid(row=1, column=1, sticky='nsew')
        self.appsFrame.config(border=5)
        self.appsFrame.columnconfigure(0, weight=100)
        self.appsFrame.columnconfigure(1, weight=1)
        self.appsFrame.rowconfigure(0, weight=100)
        self.appsFrame.rowconfigure(1, weight=1)

        self.applicationsList = tk.Listbox(self.appsFrame)
        self.applicationsList.bind('<<ListboxSelect>>', self.appSelection)
        self.applicationsList.grid(row=0, column=0, sticky='nsew')
        self.applicationsList.config(border=2, relief='sunken', font=("Purisa", 10))

        self.appsVerticalScroll = tk.Scrollbar(self.appsFrame, orient=tk.VERTICAL, command=self.applicationsList.yview)
        self.appsVerticalScroll.grid(row=0, column=1, sticky='nsw')
        self.applicationsList['yscrollcommand'] = self.appsVerticalScroll.set

        self.appsHorizontalScroll = tk.Scrollbar(self.appsFrame, orient=tk.HORIZONTAL, command=self.applicationsList.xview)
        self.appsHorizontalScroll.grid(row=1, column=0, sticky='sew')
        self.applicationsList['xscrollcommand'] = self.appsHorizontalScroll.set

        for zone in self.summedTime:
            self.applicationsList.insert(tk.END, zone[0] + ' - ' + time.strftime('%H:%M:%S', time.gmtime(zone[1])))

    def instancesFrameDeclaration(self):
        self.instancesFrame.grid(row=3, column=1, sticky='nsew')
        self.instancesFrame.config(border=5)
        self.instancesFrame.columnconfigure(0, weight=100)
        self.instancesFrame.columnconfigure(1, weight=1)
        self.instancesFrame.rowconfigure(0, weight=100)
        self.instancesFrame.rowconfigure(1, weight=1)

        self.instancesList = tk.Listbox(self.instancesFrame)
        self.instancesList.grid(row=0, column=0, sticky='nsew')
        self.instancesList.config(border=2, relief='sunken', font=("Purisa", 10))

        self.instancesVerticalScroll = tk.Scrollbar(self.instancesFrame, orient=tk.VERTICAL, command=self.instancesList.yview)
        self.instancesVerticalScroll.grid(row=0, column=1, sticky='nsw')
        self.instancesList['yscrollcommand'] = self.instancesVerticalScroll.set

        self.instancesHorizontalScroll = tk.Scrollbar(self.instancesFrame, orient=tk.HORIZONTAL, command=self.instancesList.xview)
        self.instancesHorizontalScroll.grid(row=1, column=0, sticky='sew')
        self.instancesList['xscrollcommand'] = self.instancesHorizontalScroll.set

    def drawingPieChart(self, percentage=percentageTime, totalTime=summedTime):
        fig = matplotlib.figure.Figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        ax.pie(percentage, labels=[x[0] for x in totalTime], autopct='%1.f%%', explode=[0.01 for x in totalTime], startangle=0, labeldistance=1.2)

        canvas = FigureCanvasTkAgg(fig, master=self.pieFrame)
        canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, sticky='nsew')
        canvas.draw()

    def dateSelection(self, value):
        for k in self.listOfFiles.keys():
            if k == value:
                self.applicationsList.delete(0, 'end')
                self.instancesList.delete(0, 'end')

                self.data = jO.defDecodingJson(self.listOfFiles[k])
                self.summedTime = jO.defSummingUpTotalTime(self.data)
                self.percentageTime = jO.defPercentageCalculation(self.summedTime)
                self.sortedInstances = jO.defSortedInstances(self.data)

                for zone in self.summedTime:
                    self.applicationsList.insert(tk.END, zone[0] + ' - ' + time.strftime('%H:%M:%S', time.gmtime(zone[1])))

                self.drawingPieChart(percentage=self.percentageTime, totalTime=self.summedTime)

    def appSelection(self, evt):
        self.selectedApp = str((self.applicationsList.get(self.applicationsList.curselection())))
        self.selectedApp = self.selectedApp[:-11]

        for key in self.sortedInstances.keys():
            if key == self.selectedApp:
                self.instancesList.delete(0, 'end')
                for x in range(len(self.sortedInstances[key])):
                    self.instancesList.insert(tk.END, self.sortedInstances[key][x][0] + ' - ' + time.strftime('%H:%M:%S', time.gmtime(self.sortedInstances[key][x][1])))

    def updateData(self):
        self.listOfFiles = jO.defListOfFiles()
        self.latestFile = jO.defFindingLatestFile(self.listOfFiles)

        selectedDate = self.defaultDate.get()

        if selectedDate == self.latestFile[0]:
            selection = self.selectedApp
            self.applicationsList.delete(0, 'end')
            self.instancesList.delete(0, 'end')

            self.data = jO.defDecodingJson(self.listOfFiles[selectedDate])
            self.summedTime = jO.defSummingUpTotalTime(self.data)
            self.percentageTime = jO.defPercentageCalculation(self.summedTime)
            self.sortedInstances = jO.defSortedInstances(self.data)

            for zone in self.summedTime:
                self.applicationsList.insert(tk.END, zone[0] + ' - ' + time.strftime('%H:%M:%S', time.gmtime(zone[1])))

            self.drawingPieChart(percentage=self.percentageTime, totalTime=self.summedTime)

            if selection != None:
                for key in self.sortedInstances.keys():
                    if key == selection:
                        self.instancesList.delete(0, 'end')

                        for x in range(len(self.sortedInstances[key])):
                            self.instancesList.insert(tk.END, self.sortedInstances[key][x][0] + ' - ' + time.strftime('%H:%M:%S', time.gmtime(self.sortedInstances[key][x][1])))

        root.after(300000, self.updateData)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x800")
    my_gui = MainApplication(root)
    root.mainloop()