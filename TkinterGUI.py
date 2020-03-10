from tkinter import *
from PIL import ImageTk, Image
import numpy as np
import matplotlib.pyplot as plt
from jsonOperations import defLoadDate
from jsonOperations import defSummingUpTotalTime

root = Tk()
root.title('Codemy.com - Learn to Code!')
root.geometry("400x200")

def graph():
    data = defLoadDate()
    summedTime = defSummingUpTotalTime(jsonData=data)
    house_prices = [summedTime[0][1]["Percentage time of use"], summedTime[1][1]["Percentage time of use"] , summedTime[2][1]["Percentage time of use"]]
    plt.pie(house_prices, autopct="%1.1f%%")
    plt.show()

my_button = Button(root, text = "Graph it!", command = graph)
my_button.pack()

root.mainloop()