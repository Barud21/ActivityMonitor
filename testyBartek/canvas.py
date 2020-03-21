try:
    import tkinter as tk
except ImportError: # python 2
    import Tkinter as tk

import matplotlib.figure
import matplotlib.patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from jsonOperations import defLoadDate
from jsonOperations import defSummingUpTotalTime

window= tk.Tk()

window.columnconfigure(0, weight=100)
window.columnconfigure(0, weight=100)
window.columnconfigure(0, weight=100)
window.rowconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

canvas = tk.Canvas(window, relief='raised')
canvas.grid(row=0, column=0)


data = defLoadDate()
summedTime = defSummingUpTotalTime(jsonData=data)
house_prices = [summedTime[0][1]["Percentage time of use"], summedTime[1][1]["Percentage time of use"] , summedTime[2][1]["Percentage time of use"]]

fig = matplotlib.figure.Figure(figsize=(5,5))
ax = fig.add_subplot(111)
ax.pie([summedTime[0][1]["Percentage time of use"],summedTime[1][1]["Percentage time of use"],summedTime[2][1]["Percentage time of use"]])
ax.legend([summedTime[0][0],summedTime[1][0],summedTime[2][0]])

#circle=matplotlib.patches.Circle( (0,0), 0.7, color='white')
#ax.add_artist(circle)

fig_can = FigureCanvasTkAgg(fig, master=window)
canvas.insert()
fig_can.get_tk_widget().pack()
fig_can.draw()
window.mainloop()