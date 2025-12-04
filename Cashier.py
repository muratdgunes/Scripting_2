from tkinter import *

class Cashier(Frame):
    def __init__(self,clientsocket):
        Frame.__init__(self)
        self.master.title('Transaction')  # title koymak için
        self.clientsocket = clientsocket

        # expandable
        self.master.rowconfigure(0, weight=1) # if it is non zero value it will be expandable
        self.master.columnconfigure(0, weight=1)


        for i in range(0,8):
            self.rowconfigure(i, weight=1) # we will have just 1 row. Make it expandable



        for j in range(0,2):
            self.columnconfigure(j, weight=1) # we have 3 columns, it is to make them expandable

        self.grid(sticky=W + E + N + S) # fill until the walls, have padding 20px everywhere


        self.label = Label(self, text="Book id: ")
        self.label.grid(row=0, column=0, sticky=E+W+S,pady=20) #username

        self.mainEntry = Entry(self, justify=LEFT)
        self.mainEntry.grid(row=0, column=1, columnspan=3, sticky=W+S,ipady=3,ipadx=52, padx=1,pady=20) #username entry box.



        self.label2 = Label(self, text="Quantity: ")
        self.label2.grid(row=1, column=0, sticky=E+W)

        self.mainEntry1 = Entry(self, justify=LEFT)
        self.mainEntry1.grid(row=1, column=1, columnspan=3, sticky=W, ipady=3,ipadx=52, padx=1)



        self.button = Button(self, text="Add", command = self.add)
        self.button.grid(row=2, columnspan=2, sticky=E+W+N, padx=125, pady=125, ipady=30)

        self.label3 = Label(self, text="Books Added:")
        self.label3.grid(row=3, sticky=W+E+N, columnspan=3)

        self.mainEntry1 = Entry(self, justify=LEFT)
        self.mainEntry1.grid(row=4, columnspan=2, sticky=W+E, ipady=80, padx=40, pady=40)


    def add(self):
        print("hi")
