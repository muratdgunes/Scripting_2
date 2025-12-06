from tkinter import *
from tkinter import messagebox

class Manager(Frame):
    def __init__(self,clientsocket):
        Frame.__init__(self)
        self.clientsocket = clientsocket
        self.pack()
        self.master.title("Inventory Management")

        #=====ADD BOOK İÇİN=========

        add_frame = LabelFrame(self, text="Add book",padx=15,pady=10)
        add_frame.pack()

        Add_frame1 = Frame(add_frame)
        Add_frame1.pack()

        self.book_id_Label = Label(Add_frame1,text="Book ID: ")
        self.book_id_Label.pack(padx=5,pady = 5, side=LEFT)
        self.bookid_entry = Entry(Add_frame1,width=40)
        self.bookid_entry.pack(padx=(0,5),pady=5,side= LEFT)


        Add_frame2 = Frame(add_frame)
        Add_frame2.pack()

        self.tilte_Label = Label(Add_frame2,text="Title: ")
        self.tilte_Label.pack(padx=(0,10),pady = 5, side=LEFT)
        self.title_entry = Entry(Add_frame2,width=40)
        self.title_entry.pack(padx=(15,0),pady=5,side= LEFT)


        Add_frame3 = Frame(add_frame)
        Add_frame3.pack()

        self.Authors_Label = Label(Add_frame3,text="Authors: ")
        self.Authors_Label.pack(padx=5,pady=5,side=LEFT)
        self.Authors_Entry = Entry(Add_frame3,width=40)
        self.Authors_Entry.pack(padx=(0,5),pady=5,side=LEFT)


        Add_frame4 = Frame(add_frame)
        Add_frame4.pack()

        self.Genre_Label = Label(Add_frame4,text="Genre: ")
        self.Genre_Label.pack(padx=(0,7),pady=5,side=LEFT)
        self.Genre_Entry = Entry(Add_frame4,width=40)
        self.Genre_Entry.pack(padx=(10,0),pady=5,side=LEFT)


        Add_frame5 = Frame(add_frame)
        Add_frame5.pack()

        self.Price_Label = Label(Add_frame5,text="Price: ")
        self.Price_Label.pack(padx=(0,2),pady=5,side=LEFT)
        self.Price_Entry = Entry(Add_frame5,width=40)
        self.Price_Entry.pack(padx=(17,0),pady=5,side=LEFT)

        Add_frame6 = Frame(add_frame)
        Add_frame6.pack()

        self.Quantity_Label = Label(Add_frame6,text="Quantity: ")
        self.Quantity_Label.pack(padx=(5,0),pady=5,side=LEFT)
        self.Quantity_Entry = Entry(Add_frame6,width=40)
        self.Quantity_Entry.pack(padx=(0,4),pady=5,side=LEFT)

        Add_frame7 = Frame(add_frame)
        Add_frame7.pack()

        self.Add_Button = Button(Add_frame7,width=10, text="Add",command = self.Add_ButtonPressed)
        self.Add_Button.pack(padx=(275,0), pady=5, side=LEFT)

        #=====Update BOOK İÇİN=========


        update_frame = LabelFrame(self, text="Update Inventory",padx=15,pady=10)
        update_frame.pack()

        Update_frame1 = Frame(update_frame)
        Update_frame1.pack()
        self.update_bookID_Label = Label(Update_frame1,text="Book ID:")
        self.update_bookID_Label.pack(padx=(5,45),pady=5,side=LEFT)
        self.update_bookId_entry = Entry(Update_frame1,width=25)
        self.update_bookId_entry.pack(padx=(50,0),pady=5,side=LEFT)

        Update_frame2 = Frame(update_frame)
        Update_frame2.pack()
        self.update_Number_of_books_Label = Label(Update_frame2,text="# of books to be added ")
        self.update_Number_of_books_Label.pack(padx=5,pady=5,side=LEFT)
        self.update_Number_of_books_entry = Entry(Update_frame2,width=25)
        self.update_Number_of_books_entry.pack(padx=(10,0),pady=5,side=LEFT)

        Update_frame3 = Frame(update_frame)
        Update_frame3.pack()

        self.Update_Button = Button(Update_frame3,width=10, text="Update",command = self.Update_ButtonPressed)
        self.Update_Button.pack(padx=(275,0), pady=5, side=LEFT)


        #Statisc için

        Statistics_frame = LabelFrame(self, text="Statistics",padx=15,pady=10)
        Statistics_frame.pack()

        self.statistics_choice = StringVar()
        self.statistics_choice.set("Top-Selling Author")

        Statistics_frame1 = Frame(Statistics_frame)
        Statistics_frame1.pack(padx=(0,175))
        
        self.Top_Sellings = Radiobutton(Statistics_frame1, text="Top-Selling Author", variable=self.statistics_choice,value="Top-Selling Author")
        self.Top_Sellings.pack(padx=5, pady=5, side=LEFT)

        Statistics_frame2 = Frame(Statistics_frame)
        Statistics_frame2.pack(padx=(0,160))

        self.Most_Profitable_Genre = Radiobutton(Statistics_frame2, text="Most Profitable Genre", variable=self.statistics_choice,value="Most Profitable Genre")
        self.Most_Profitable_Genre.pack(padx=5, pady=5, side=LEFT)

        Statistics_frame3 = Frame(Statistics_frame)
        Statistics_frame3.pack(padx=(0,195))

        self.Busiest_Cashier = Radiobutton(Statistics_frame3, text="Busiest Cashier", variable=self.statistics_choice,value="Busiest Cashier")
        self.Busiest_Cashier.pack(padx=5, pady=5, side=LEFT)

        Statistics_frame4 = Frame(Statistics_frame)
        Statistics_frame4.pack()

        self.Generate_Button = Button(Statistics_frame4,width=10, text="Generate", command = self.Generate_ButtonPressed)
        self.Generate_Button.pack(padx=(275,0), pady=5, side=LEFT)
        
        CloseeFrame = Frame(self)
        CloseeFrame .pack()
        self.Close_Button = Button(CloseeFrame, text="Close",width=10,command= self.Exit)
        self.Close_Button.pack(padx=5, pady=5, side=LEFT)

    def Add_ButtonPressed(self):
        added_book_id = self.bookid_entry.get()
        added_title =  self.title_entry.get()
        added_authors=  self.Authors_Entry.get()
        added_Genre = self.Genre_Entry.get()
        added_Price = self.Price_Entry.get()
        added_Quantity = self.Quantity_Entry.get()


        new_book =f"addbook;{added_book_id};{added_title};{added_authors};{added_Genre};{added_Price};{added_Quantity};".encode()
        self.clientsocket.send(new_book)
    
    def Update_ButtonPressed(self):
        updated_book_id = self.update_bookId_entry.get()
        updated_Number_of_Books = self.update_Number_of_books_entry.get()

        updated_book = f"updatequantity;{updated_book_id};{updated_Number_of_Books}".encode()
        self.clientsocket.send(updated_book)

    def Generate_ButtonPressed(self):
        generated_statistics = self.statistics_choice.get()

        if (generated_statistics == "Top-Selling Author"):
            report_code = "report1".encode()
            self.clientsocket.send(report_code)
            data = self.clientsocket.recv(1024).decode()

        elif (generated_statistics == "Most Profitable Genre"):
            report_code = "report2".encode()
            self.clientsocket.send(report_code)
            data = self.clientsocket.recv(1024).decode()
            
        else:
            report_code = "report3".encode()
            
        self.clientsocket.send(report_code)
        data = self.clientsocket.recv(1024).decode()
        parts = data.split(";")

        if parts[0].startswith("report"):
            if len(parts) == 2:
                messagebox.showinfo("Statistics Result", parts[1])
            else:
                answers = "\n".join(parts[1:])
                messagebox.showinfo("Statistics Result", answers)

    def Exit(self):
        msg = "closeconnection".encode()
        self.clientsocket.send(msg)
        self.master.destroy()

    







        












        






if __name__ == "__main__":
    window = Manager()
    window.mainloop()
