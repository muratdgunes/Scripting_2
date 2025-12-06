from socket import *
from Login import *


HOST = "127.0.0.1"
PORT = 5000

client = socket(AF_INET, SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    in_data = client.recv(1024).decode()

    in_data = in_data.split(";")

    if in_data[0] == "connectionsuccess":
        print("Successfully connected.")
        c = Login(client)   # LOGIN SCREEN START------
        c.master.geometry("395x210")
        c.mainloop()    # LOGIN SCREEN END------
    else:
        print("connection failed... try again later")
        break
client.close()