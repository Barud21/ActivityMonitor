import tkinter as tk
import matplotlib.figure
import matplotlib.patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import jsonOperations as jO

window = tk.Tk()
window.title('Activity Monitor')

window.columnconfigure(0, weight=10000)
window.columnconfigure(1, weight=10000)
window.columnconfigure(2, weight=1)
window.columnconfigure(3, weight=10000)
window.columnconfigure(4, weight=1)
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1000000)
window.rowconfigure(1, weight=1)
label = tk.Label(window, text = "Hello World")
label.grid(row=0, column=0)

# TODO: Add element to choose a file
data = jO.defDecodingJson()
summedTime = jO.defSummingUpTotalTime(data)
percentageTime = jO.defPercentageCalculation(summedTime)
sortedInstances = jO.defSortedInstances(data)

house_prices = percentageTime

fig = matplotlib.figure.Figure(figsize=(5,5))
ax = fig.add_subplot(111)
ax.pie(percentageTime)
ax.legend([x[0] for x in summedTime]) # summedTime[0][0]

canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().grid(row=1, column=0, sticky='nsew')
canvas.draw()

applicationList = tk.Listbox(window)
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

instancesList = tk.Listbox(window)
instancesList.grid(row=1, column=3, sticky='nsew')
instancesList.config(border=2, relief='sunken')
for key in sortedInstances.keys():
    for x in range(len(sortedInstances[key])):
        instancesList.insert(tk.END, sortedInstances[key][x][0] + ' - ' + time.strftime('%H:%M:%S', time.gmtime(sortedInstances[key][x][1])))

instancesScrollVertical = tk.Scrollbar(window, orient=tk.VERTICAL, command=instancesList.yview)
instancesScrollVertical.grid(row=1, column=4, sticky='nsw')
instancesList['yscrollcommand'] = instancesScrollVertical.set

instancesScrollHorizontal = tk.Scrollbar(window, orient=tk.HORIZONTAL, command=instancesList.xview)
instancesScrollHorizontal.grid(row=2, column=3, sticky='sew')
instancesList['xscrollcommand'] = instancesScrollHorizontal.set

window.mainloop()