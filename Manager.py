from tkinter import *
from tkinter import messagebox

class Manager(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.pack()
        self.master.title("Inventory Management")

        self.frame1 = Frame(self)
        self.frame1.pack(padx=150, pady=275)

        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        for i in range(0,5):
            self.rowconfigure(i, weight=1)

        for j in range(0,4):
            self.columnconfigure(j, weight=1)
        
        self.label = Label(self, text = "Add Book")




if __name__ == "__main__":
    window = Manager()
    window.mainloop()
