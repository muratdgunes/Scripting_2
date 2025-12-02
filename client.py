from socket import *
from threading import *
from tkinter import *
from tkinter import messagebox


HOST = "127.0.0.1"
PORT = 5000

client = socket(AF_INET, SOCK_STREAM)
client.connect((HOST, PORT))

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
        client.send(msg) # send login details to server

        response = self.clientsocket.recv(1024).decode() #wait for server response

        response = response.split(";") # parse response
        if response[0] == "loginsuccess":
            print(response)
            messagebox.showinfo("Login Successful",f"Login successful, Welcome {response[1]}")
            self.master.destroy()

            #roleUser = userDictionary[response[1]]["role"] dont do this, negative marks security concerns

            if response[2] == "Cashier":
                z = Cashier(client)
                z.master.geometry("400x750")
                z.mainloop()
            else:
                print("show manager frame-----------")
        else:
            print("Response from server: \"",response,"\" Please try again...")
            messagebox.showinfo("Login Failed", "Login failed, Please try again...")



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




while True:
    in_data = client.recv(1024).decode()
    print("Message received: ", in_data)
    in_data = in_data.split(";")
    print("Parsed message is: ", in_data)
    #out_data = input("Enter your question: ")
    #client.send(out_data.encode())
    if in_data[0] == "connectionsuccess":
        print("Successfully connected.")
        c = Login(client)   # LOGIN SCREEN START------
        c.master.geometry("395x210")
        c.mainloop()    # LOGIN SCREEN END------



        #break

    else:
        print("connection failed... try again later")
        #break

client.close()