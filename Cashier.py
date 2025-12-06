from tkinter import *
from tkinter import messagebox

class Cashier(Frame):
    def __init__(self,clientsocket):
        Frame.__init__(self)
        self.master.title('Transaction')  # for placing title.
        self.clientsocket = clientsocket  # initialize client socket
        self.count = 0

        self.pack()

        self.frame1 = Frame(self) # frame 1 start -------------------------
        self.frame1.pack(padx=5, pady=25)

        self.label = Label(self.frame1, text="Book id: ")
        self.label.pack(padx=(20,8), pady=5, side=LEFT)

        self.mainEntry = Entry(self.frame1)
        self.mainEntry.pack(padx=(5,25), pady=5, side=LEFT,ipadx=70,ipady=3)
        # frame 1 end --------------------------------------------------------



        self.frame2 = Frame(self) # frame 2 start ---------------------
        self.frame2.pack(padx=5, pady=5)

        self.label2 = Label(self.frame2, text="Quantity: ")
        self.label2.pack(padx=(20,5), pady=5, side=LEFT)

        self.mainEntry1 = Entry(self.frame2, justify=LEFT)
        self.mainEntry1.pack(padx=(5,25), pady=5, side=LEFT, ipadx=70, ipady=3)
        # frame 2 end -------------------------------------------------

        self.frame3 = Frame(self) # frame 3 start ---------------
        self.frame3.pack(padx=5, pady=5)

        self.button = Button(self.frame3, text="Add", command = self.add)
        self.button.pack(ipadx=35,ipady=5, side=TOP,pady=(20,0))
        # frame 3 end -------------------------------------------


        self.frame4 = Frame(self) # frame 4 start -------------------
        self.frame4.pack(padx=5, pady=5)

        self.label3 = Label(self.frame4, text="Books Added:")
        self.label3.pack(padx=25, pady=(25,0), side=LEFT)
        # frame 4 end -----------------------------------------------


        self.frame5 = Frame(self) # frame 5 start -----------------------
        self.frame5.pack(padx=5, pady=5)

        self.mainEntry3 = Listbox(self.frame5) # listbox is used because it automatically formats. And it is easy to read from.
        self.mainEntry3.pack(padx=5, pady=5, side=LEFT, ipadx=82)
        # frame 5 end ---------------------------------------------------


        self.frame6 = Frame(self) # frame 6 start --------------------
        self.frame6.pack(padx=5, pady=5)

        self.label4 = Label(self.frame6, text="Discount Code: ")
        self.label4.pack(padx=(20,3), pady=(5,25), side=LEFT)

        self.mainEntry4 = Entry(self.frame6, justify=LEFT)
        self.mainEntry4.pack(padx=(5,25), pady=(5,25), side=LEFT, ipadx=55, ipady=3)
        # frame 6 end ------------------------------------------------


        self.frame7 = Frame(self) # frame 7 start --------------------
        self.frame7.pack(padx=5, pady=5)

        self.button1 = Button(self.frame7, text="Close", command=self.close)
        self.button1.pack(padx=(60,0),pady=(3,20),side=LEFT,ipadx=35,ipady=5)

        self.button2 = Button(self.frame7, text="Complete Transaction", command=self.complete)
        self.button2.pack(padx=20, side=LEFT, ipadx=35,ipady=5,pady=(3,20))
        # frame 7 end ------------------------------------------------

    def close(self):

        self.master.destroy()
        self.clientsocket.close()

    def add(self):
        book_id = self.mainEntry.get()
        quantity = self.mainEntry1.get()

        self.mainEntry.delete(0,END)
        self.mainEntry1.delete(0,END)

        self.mainEntry3.insert(END, f"{book_id}-{quantity}\n")
        self.count+=1   # every time an item is added, increase the count.

    def complete(self):
        i=0
        message_to_be_sent ="transaction;"
        temp =""

        discount = self.mainEntry4.get() # get the discount code entry.

        if discount != "":  # if discount entry is filled, also add it to the message to be sent to server.
            message_to_be_sent += discount

        while self.count > i: # iterate until all items are processed.
            line = self.mainEntry3.get(first=i) # read the listbox.

            if line not in temp: # parse the data read from the listbox.
                if line =="":
                    break   # reading from listbox resulted in an extra item which is "". This line will discard that.
                else:
                    temp += line
            i+=1

        temp = temp.split("\n") # split the message received from listbox.

        for each in temp:   # check if item is in needed format. Ex: "1001-2" , "1002-5"
            if each == "":
                continue   # to not add newline character to "message_to_be_sent" which will be sent to server.

            message_to_be_sent += f";{each}"

        self.count = 0 # reset the counter that counts listbox items.
        self.mainEntry.delete(0, END)
        self.mainEntry1.delete(0, END)
        self.mainEntry3.delete(0, END)
        self.mainEntry4.delete(0, END)

        print("Cashier>>",message_to_be_sent)
        msg = message_to_be_sent.encode()
        self.clientsocket.send(msg) # send the transaction details to the server

        data = self.clientsocket.recv(1024).decode() # wait for response from the server
        print("Server>>",data)
        data = data.split(";") # parse the response

        if data[0] == "transactionfailure":
            messagebox.showinfo("Transaction Failure", data[1])

        elif data[0] == "transactionconfirmation":
            messagebox.showinfo("Successful Transaction", "Total price is: "+data[1])



