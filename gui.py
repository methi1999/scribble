"""
ITSP 2018
Scribble by Four-Play

A GUI program which updates the text label
Run this parallely with the master

"""

import tkinter as tk
import pickle
import time

#Milliseconds after which the label should be updated
freq=500

#Function which changes the label
def change_label(label):
  def change():
  	#Read dumped string
    s=pickle.load(open('finalstring.p','rb'))
    label.config(text=s,font=(None,75),width=50)
    label.after(freq, change)
    # print("Hey")
  change()
 
 #Initialize GUI
root = tk.Tk()
root.title("Current Text")
label = tk.Label(root, fg="green")
label.pack()
change_label(label)
# s=pickle.load(open('finalstring.p','rb'))

