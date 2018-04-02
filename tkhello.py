#from Tkinter import *
#
#root = Tk()
#
#w = Label(root, text="Hello, world!")
#w.pack()
#
#root.mainloop()

#Added this line to test closing and opening atom
#Adding this line to test pulling from a different machine

import Tkinter as tk

root = tk.Tk()

root.geometry("100x100")
root.resizable(0, 1) #Don't allow resizing in the x or y direction

label = tk.Label(root, text="Hello World", padx=20, pady=20)
label.pack()

root.mainloop()
