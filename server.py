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
                inventoryDictionary = {}
                discountCodes = []

                # print("at transaction, parsed data is: ",parsed_data)
                with open("discountcodes.txt", "r", encoding="utf-8") as file1:
                    for line in file1:
                        line = line.split(" ")
                        discountCodes.append(line[0])

                # print(discountCodes)
                with open("inventory.txt", "r", encoding="utf-8") as file2:
                    for line in file2:
                        line = line.split(";")
                        if len(line) == 6:
                            bookID = line[0]
                            bookName = line[1]
                            authors = line[2]
                            genre = line[3]
                            price = line[4]
                            tempAmount = line[5].split("\n")
                            amount = tempAmount[0]
                            inventoryDictionary[bookID] = {"name": bookName, "authors": authors, "genre": genre,
                                                           "price": price, "amount": amount}
                print("parsed data is: ", parsed_data)
                if parsed_data[1] not in discountCodes and parsed_data[1] != "":
                    msg = "transactionfailure;Invalid discount code.".encode()
                    self.clientsocket.send(msg)


                else:
                    i = 0
                    totalPrice = 0
                    inputLength = len(parsed_data)

                    fail = 0  # initially there is no fail.
                    pattern = r"([0-9]+)-([0-9]+)"  # pattern to check if input is acceptable. Format example: "1001-5"
                    while i < inputLength - 2:  # -2 because first two values in parsed data are reserved for [server tag(Ex: transaction) and discount code]. Therefore, we will just iterate the loop -2 times.

                        spot = re.match(pattern, parsed_data[
                            i + 2])  # assuming the pattern is always in this format: (Ex: "1001-2"). As provided txt file suggests.
                        if not spot:
                            msg = f"transactionfailure;Input has missing information of wrong format!\nPlease try again...".encode()
                            self.clientsocket.send(msg)
                            fail = 1
                            break  # break point [a]

                        parsed_data[i + 2] = parsed_data[i + 2].split(
                            "-")  # split data into format: ("book ID", "amount")
                        if parsed_data[i + 2][0] not in inventoryDictionary:
                            msg = f"transactionfailure;Book with specified ID does not exist in the database!\nBook {parsed_data[i + 2][0]} is not found.".encode()
                            self.clientsocket.send(msg)
                            fail = 1
                            break  # break point [b]

                        bookID = int(parsed_data[i + 2][0])
                        parsed_amount = int(parsed_data[i + 2][1])
                        dict_amount = int(inventoryDictionary[parsed_data[i + 2][0]]["amount"])

                        if dict_amount < parsed_amount:  # means if [inventory amount < requested amount] enter here.
                            msg = f"transactionfailure;Inventory does not have required amount of book(s).\nfor book {bookID}:\ninventory has {dict_amount} books, requested amount is {parsed_amount}".encode()
                            self.clientsocket.send(msg)  # send failure message to client.
                            fail = 1  # fail occurred, break from the current loop and continue from the bigger loop.
                            break  # break point [c]

                        itemPrice = float(
                            inventoryDictionary[parsed_data[i + 2][0]]["price"])  # get the price of the current book.
                        itemPrice = float(itemPrice) * int(parsed_data[i + 2][1])  # multiply book price and amount.
                        totalPrice += itemPrice  # add to total price

                        i += 1  # increase the i so that next [bookID-amount] pair is processed.

                    if fail == 1:  # after break at [a], [b] or [c], program will come here. If fail is 1 server will continue from the beginning.
                        continue  # at the beginning server will wait for user input.

                    if parsed_data[1] == "":
                        print("total price is: ", totalPrice)
                        msg = f"transactionconfirmation;{totalPrice:.2f}".encode()
                        self.clientsocket.send(msg)
                    else:
                        # delete code
                        msg = f"transactionconfirmation;{(totalPrice * 0.9):.2f}".encode()
                        self.clientsocket.send(msg)

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
                results = self.compute_top_selling_author()
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




    def compute_top_selling_author(self):
        inv = {}  # bookid → authors
        with open("inventory.txt", "r", encoding="utf-8") as file:
            for line in file:
                fields = line.strip().split(";")
                bookid = fields[0]
                authors = fields[2]
                inv[bookid] = authors

        book_to_authors ={}
        with open("transactions.txt", "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(";")

                for item in parts[4:]:
                    bookid, quantity = item.split("-")
                    quantity = int(quantity)

                    if bookid in inv:
                        authors_key = inv[bookid]
                        author = authors_key.split(" and ")

                    for a in author:
                        book_to_authors[a] = book_to_authors.get(a,0) + quantity
        Top_sell = max(book_to_authors.values())
        result = [a for a in book_to_authors if book_to_authors[a] == Top_sell]
        return result

    @staticmethod
    def compute_most_profitable_genre():
            book_info = {}

    @staticmethod
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









HOST = "10.143.17.186"

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

