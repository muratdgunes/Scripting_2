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


class ClientThread(Thread):
    def __init__(self, clientsocket, clientaddress):
        Thread.__init__(self)
        self.clientsocket = clientsocket
        self.clientaddress = clientaddress
        msg = "connectionsuccess".encode()
        self.clientsocket.send(msg)
        print("Connection From ", clientaddress)

    def run(self):
        print("THread started")
        count = 0
        while True:
            data = self.clientsocket.recv(1024).decode()
            print(data)
            count+=1
            parsed_data = data.split(";")
            print(parsed_data)
            if parsed_data[0] == "login":
                if parsed_data[1] in userDictionary:
                    msg = f"loginsuccess;{parsed_data[1]};{userDictionary[parsed_data[1]]["role"]}".encode()
                    self.clientsocket.send(msg)
                else:
                    msg = "loginfailure".encode()
                    self.clientsocket.send(msg)

            elif parsed_data[0] == "transaction":
                print("at transaction.")

            elif parsed_data[0] == "addbook":

                book_id = parsed_data[1]
                title = parsed_data[2]
                authors = parsed_data[3] 
                genre = parsed_data[4]
                price = parsed_data[5]
                quantity =parsed_data[6]

                with open("inventory.txt","a", encoding="utf-8") as file:
                    file.write(f"\n{book_id};{title};{authors};{genre};{price};{quantity}")
            
                clientsocket.send("addbookconfirmation".encode())
   
            elif parsed_data[0] == "updatequantity":
                book_id = parsed_data[1]
                new_quantitiy = parsed_data[2]

                updated_line = []
                found = False

                with open("inventory.txt","r", encoding="utf-8") as file:
                    for line in file:
                        fields = line.strip().split(";")

                        if(fields[0]==book_id):
                            fields[5] = str(int(fields[5]) + int(new_quantitiy))
                            found = True

                        updated_line.append(";".join(fields))
                with open("inventory.txt","w", encoding="utf-8") as file:
                    index = 0
                    total = len(updated_line)
                    for line in updated_line:
                        if index<total -1:
                            file.write(line + "\n")
                        else:
                            file.write(line)
                        index +=1

                if found:
                    clientsocket.send("updatequantityconfirmation".encode())
                else:
                    clientsocket.send("updatequantityfailed".encode())


            
            elif parsed_data[0] == "report1":
                results = ClientThread.compute_top_selling_author()
                reponse ="report1;" + ";".join(results)
                clientsocket.send(reponse.encode())
            elif parsed_data[0] == "report2":
                results = ClientThread.compute_most_profitable_genre()
                clientsocket.send(("report2;"+ ";".join(results)).encode())
            elif parsed_data[0] == "report3":
                results = ClientThread.compute_busiest_cashier()
                clientsocket.send(("report3;"+";".join(results)).encode())
        
            elif parsed_data[0] == "Close":
                self.clientsocket.close()
                break


    def load_inventory():
        inv = {}  # bookid → authors
        with open("inventory.txt", "r", encoding="utf-8") as file:
            for line in file:
                fields = line.strip().split(";")
                bookid = fields[0]
                authors = fields[2]
                inv[bookid] = authors
        return inv


    def compute_top_selling_author():
        inventory = ClientThread.load_inventory()
        book_to_authors ={}
        with open("transactions.txt", "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(";")

                for item in parts[4:]:
                    bookid, quantity = item.split("-")
                    quantity = int(quantity)

                    if bookid in inventory:
                        authors_key = inventory[bookid]
                        author = authors_key.split(" and ")

                    for a in author:
                        book_to_authors[a] = book_to_authors.get(a,0) + quantity
        Top_sell = max(book_to_authors.values())
        result = [a for a in book_to_authors if book_to_authors[a] == Top_sell]
        return result

    
    def compute_most_profitable_genre():
            book_info = {}

    def compute_busiest_cashier():

        cashier_counts = {}  

        with open("transactions.txt", "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(";")
                cashier = parts[0]
                cashier_counts[cashier] = cashier_counts.get(cashier, 0) + 1 #I got help here from chat gpt and I learnt that notation which is cashier_counts.get(cashier, 0) + 1

        busiest = max(cashier_counts.values())
        result = [c for c in cashier_counts if cashier_counts[c] == busiest]

        return result









HOST = "127.0.0.1"

PORT = 5000

server = socket(AF_INET, SOCK_STREAM)# addres family afinet, port number sock stream

server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # this socket is reusable by multiple clients 1-reusable

server.bind((HOST, PORT))
print("Server started")
print("Waiting for connection request")
count =0



while True:
    server.listen()
    clientsocket, clientaddress = server.accept()
    newThread = ClientThread(clientsocket, clientaddress)
    newThread.start()

