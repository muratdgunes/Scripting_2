from tkinter import *
from tkinter import messagebox
from Cashier import Cashier
from Manager import Manager
class Login(Frame):
    def __init__(self,clientsocket):
        Frame.__init__(self)
        self.master.title('Login')  # title koymak için
        self.clientsocket = clientsocket

        # expandable
        self.master.rowconfigure(0, weight=1) # if it is non zero value it will be expandable
        self.master.columnconfigure(0, weight=1)


        for i in range(0,3):
            self.rowconfigure(i, weight=1) # we will have just 1 row. Make it expandable



        for j in range(0,2):
            self.columnconfigure(j, weight=1) # we have 3 columns, it is to make them expandable

        self.grid(sticky=W + E + N + S) # fill until the walls, have padding 20px everywhere


        self.label = Label(self, text="Username:")
        self.label.grid(row=0, column=0, sticky=E+W+S,pady=20) #username

        self.mainEntry = Entry(self, justify=LEFT)
        self.mainEntry.grid(row=0, column=1, columnspan=3, sticky=W+S,ipady=3,ipadx=52, padx=1,pady=20) #username entry box.



        self.label2 = Label(self, text="Password:")
        self.label2.grid(row=1, column=0, sticky=E+W)

        self.mainEntry1 = Entry(self, justify=LEFT)
        self.mainEntry1.grid(row=1, column=1, columnspan=3, sticky=W, ipady=3,ipadx=52, padx=1)



        self.button = Button(self, text="Login", command = self.calculate)
        self.button.grid(row=3, column=1, padx=(5,50), ipadx=35, sticky=N+E, pady=(0,50))

    def calculate(self):
        uName = self.mainEntry.get()
        uPassword = self.mainEntry1.get()

        self.mainEntry.delete(0, END)
        self.mainEntry1.delete(0,END)
        print(uName,uPassword)
        msg = f"login;{uName};{uPassword}".encode()
        self.clientsocket.send(msg) # send login details to server

        response = self.clientsocket.recv(1024).decode() #wait for server response

        response = response.split(";") # parse response
        if response[0] == "loginsuccess":
            print(response)
            messagebox.showinfo("Login Successful",f"Login successful, Welcome {response[1]}")
            self.master.destroy()

            #roleUser = userDictionary[response[1]]["role"] dont do this, negative marks security concerns

            if response[2] == "Cashier":
                z = Cashier(self.clientsocket)
                z.master.geometry("400x750")
                z.mainloop()
            else:
                print("show manager frame-----------")
                z = Manager(self.clientsocket)
                z.master.geometry("400x750")
                z.mainloop()
        else:
            print("Response from server: \"",response,"\" Please try again...")
            messagebox.showinfo("Login Failed", "Login failed, Please try again...")