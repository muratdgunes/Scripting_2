from socket import *
from threading import *
from tkinter import *
from tkinter import messagebox
import re


userDictionary={}
with open("users.txt", "r", encoding="utf-8") as file:
    for line in file:
        pattern = r"([A-Za-z ]+);([a-zA-Z0-9 ]+);([a-zA-Z]+)"
        spot = re.match(pattern, line)

        if spot:
            name = spot.group(1)
            password = spot.group(2)
            role = spot.group(3) # parse the read user line.
            userDictionary[name] = {"password": password, "role": role}
            print(userDictionary)


class ClientThread(Thread):
    def __init__(self, clientsocket, clientaddress):
        Thread.__init__(self)
        self.clientsocket = clientsocket
        self.clientaddress = clientaddress
        print("Connection From ", clientaddress)

    def run(self):
        msg = "Welcome".encode()
        self.clientsocket.send(msg)
        count = 0
        while True:
            data = self.clientsocket.recv(1024).decode()
            print(data)
            count+=1
            if count ==3:
                break       # thread'in ne yapacağına sonra karar veririz şimdilik dursun

        self.clientsocket.close()


class Login(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title('Login')  # title koymak için


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

        if uName in userDictionary:
            if userDictionary[uName]["password"]==uPassword:
                messagebox.showinfo(f"Login Successful!", f"Welcome {uName}")

            else:
                messagebox.showinfo(f"Login Failed!", f"Password is wrong, try again...")

        else:
            messagebox.showinfo(f"Login Failed!", f"There is no user named \"{uName}\"")




c = Login()
c.master.geometry("395x210")
c.mainloop()

HOST = "127.0.0.1"

PORT = 5000

server = socket(AF_INET, SOCK_STREAM)# addres family afinet, port number sock stream

server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # this socket is reusable by multiple clients 1-reusable

server.bind((HOST, PORT))
print("Server started")
print("Waiting for connection request")
count =0



while True:
    if "john" in userDictionary:
        print(userDictionary["john"]["password"])
    count+=1
    if count==3:
        break
    #server.listen()
    #clientsocket, clientaddress = server.accept()
    #newThread = ClientThread(clientsocket, clientaddress)
    #newThread.start()

