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

data = defLoadDate()
summedTime = defSummingUpTotalTime(jsonData=data)
house_prices = [summedTime[0][1]["Percentage time of use"], summedTime[1][1]["Percentage time of use"] , summedTime[2][1]["Percentage time of use"]]

fig = matplotlib.figure.Figure(figsize=(5,5))
ax = fig.add_subplot(111)
ax.pie([summedTime[0][1]["Percentage time of use"],summedTime[1][1]["Percentage time of use"],summedTime[2][1]["Percentage time of use"]])
ax.legend([summedTime[0][0],summedTime[1][0],summedTime[2][0]])

#circle=matplotlib.patches.Circle( (0,0), 0.7, color='white')
#ax.add_artist(circle)

window= tk.Tk()
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack()
canvas.draw()
window.mainloop()