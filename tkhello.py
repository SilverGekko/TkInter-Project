#Expanding on Example 1.2

import Tkinter as tk

class Root(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.label = tk.Label(self, text="Hello World", padx=20, pady=20)
        self.geometry("400x100")
        self.minsize(400, 100)
        self.resizable(0, 1) #Don't allow resizing in the x or y direction
        self.label.pack()

if __name__ == "__main__":
    root = Root()
    root2 = Root()
    root2.mainloop()
    root.mainloop()
