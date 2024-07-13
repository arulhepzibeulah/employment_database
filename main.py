from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY, name TEXT, doj TEXT, email TEXT, gender TEXT, contact TEXT, address TEXT)"
        )
        self.conn.commit()

    def insert(self, name, doj, email, gender, contact, address):
        self.cur.execute(
            "INSERT INTO employees (name, doj, email, gender, contact, address) VALUES (?, ?, ?, ?, ?, ?)",
            (name, doj, email, gender, contact, address),
        )
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM employees")
        rows = self.cur.fetchall()
        return rows

    def remove(self, id):
        self.cur.execute("DELETE FROM employees WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, name, doj, email, gender, contact, address):
        self.cur.execute(
            "UPDATE employees SET name = ?, doj = ?, email = ?, gender = ?, contact = ?, address = ? WHERE id = ?",
            (name, doj, email, gender, contact, address, id),
        )
        self.conn.commit()

# Instantiate the database
db = Database("Employee.db")

# Tkinter Setup
root = Tk()
root.title("Employee Management System")
root.geometry("1920x1080+0+0")
root.config(bg="#2c3e50")
root.state("zoomed")

# Entry Frame
name = StringVar()
doj = StringVar()
gender = StringVar()
email = StringVar()
contact = StringVar()

# Entries Frame
entries_frame = Frame(root, bg="#535c68")
entries_frame.pack(side=TOP, fill=X)
title = Label(entries_frame, text="Employee Management System", font=("Calibri", 18, "bold"), bg="#535c68", fg="white")
title.grid(row=0, columnspan=2, padx=10, pady=20)

lblName = Label(entries_frame, text="Name", font=("Calibri", 16), bg="#535c68", fg="white")
lblName.grid(row=1, column=0, padx=10, pady=10, sticky="w")
txtName = Entry(entries_frame, textvariable=name, font=("Calibri", 16), width=30)
txtName.grid(row=1, column=1, padx=10, pady=10, sticky="w")

lbldoj = Label(entries_frame, text="D.O.J", font=("Calibri", 16), bg="#535c68", fg="white")
lbldoj.grid(row=2, column=0, padx=10, pady=10, sticky="w")
txtdoj = Entry(entries_frame, textvariable=doj, font=("Calibri", 16), width=30)
txtdoj.grid(row=2, column=1, padx=10, pady=10, sticky="w")

lblemail = Label(entries_frame, text="Email", font=("Calibri", 16), bg="#535c68", fg="white")
lblemail.grid(row=2, column=2, padx=10, pady=10, sticky="w")
txtemail = Entry(entries_frame, textvariable=email, font=("Calibri", 16), width=30)
txtemail.grid(row=2, column=3, padx=10, pady=10, sticky="w")

lblgender = Label(entries_frame, text="Gender", font=("Calibri", 16), bg="#535c68", fg="white")
lblgender.grid(row=3, column=0, padx=10, pady=10, sticky="w")
comboGender = ttk.Combobox(entries_frame, font=("Calibri", 16), width=28, textvariable=gender, state="readonly")
comboGender['values'] = ("Male", "Female")
comboGender.grid(row=3, column=1, padx=10, sticky="w")

lblcontact = Label(entries_frame, text="Contact No", font=("Calibri", 16), bg="#535c68", fg="white")
lblcontact.grid(row=3, column=2, padx=10, pady=10, sticky="w")
txtcontact = Entry(entries_frame, textvariable=contact, font=("Calibri", 16), width=30)
txtcontact.grid(row=3, column=3, padx=10, pady=10, sticky="w")

lblAddress = Label(entries_frame, text="Address", font=("Calibri", 16), bg="#535c68", fg="white")
lblAddress.grid(row=4, column=0, padx=10, pady=10, sticky="w")

txtAddress = Text(entries_frame, width=85, height=5, font=("Calibri", 16))
txtAddress.grid(row=5, column=0, columnspan=4, padx=10, sticky="w")

def getData(event):
    selected_row = tv.focus()
    data = tv.item(selected_row)
    global row
    row = data["values"]
    print(f"Selected row data: {row}")  # Debug print
    name.set(row[1])
    doj.set(row[2])
    email.set(row[3])
    gender.set(row[4])
    contact.set(row[5])
    txtAddress.delete(1.0, END)
    txtAddress.insert(END, row[6])

def displayAll():
    tv.delete(*tv.get_children())
    for row in db.fetch():
        tv.insert("", END, values=row)

def add_employee():
    print("Adding employee...")  # Debug print
    if txtName.get() == "" or txtdoj.get() == "" or txtemail.get() == "" or comboGender.get() == "" or txtcontact.get() == "" or txtAddress.get(1.0, END).strip() == "":
        messagebox.showerror("Error in Input", "Please fill all the details")
        return
    db.insert(txtName.get(), txtdoj.get(), txtemail.get(), comboGender.get(), txtcontact.get(), txtAddress.get(1.0, END))
    messagebox.showinfo("Success", "Record Inserted")
    ClearAll()
    displayAll()

def Update_employee():
    print("Updating employee...")  # Debug print
    if txtName.get() == "" or txtdoj.get() == "" or txtemail.get() == "" or comboGender.get() == "" or txtcontact.get() == "" or txtAddress.get(1.0, END).strip() == "":
        messagebox.showerror("Error in Input", "Please fill all the details")
        return
    db.update(row[0], txtName.get(), txtdoj.get(), txtemail.get(), comboGender.get(), txtcontact.get(), txtAddress.get(1.0, END))
    messagebox.showinfo("Success", "Record Updated")
    ClearAll()
    displayAll()

def Delete_employee():
    print("Deleting employee...")  # Debug print
    db.remove(row[0])
    ClearAll()
    displayAll()

def ClearAll():
    print("Clearing all fields...")  # Debug print
    name.set("")
    doj.set("")
    gender.set("")
    email.set("")
    contact.set("")
    txtAddress.delete(1.0, END)

btn_frame = Frame(entries_frame, bg="#535c68")
btn_frame.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="w")
btn_Add = Button(btn_frame, command=add_employee, text="Add Details", width=15, font=("Calibri", 16, "bold"), fg="white",
                 bg="#16a085", bd=0)
btn_Add.grid(row=0, column=0)
btn_update = Button(btn_frame, command=Update_employee, text="Update Details", width=15, font=("Calibri", 16, "bold"),
                    fg="white", bg="#2980b9", bd=0)
btn_update.grid(row=0, column=1, padx=10)
btn_Delete = Button(btn_frame, command=Delete_employee, text="Delete Details", width=15, font=("Calibri", 16, "bold"), fg="white",
                    bg="#c0392b", bd=0)
btn_Delete.grid(row=0, column=2, padx=10)
btn_Clear = Button(btn_frame, command=ClearAll, text="Clear Details", width=15, font=("Calibri", 16, "bold"), fg="white",
                   bg="#f39c12", bd=0)
btn_Clear.grid(row=0, column=3, padx=10)

tree_frame = Frame(root, bg="#ecf0f1")
tree_frame.place(x=0, y=480, width=1980, height=520)
style = ttk.Style()
style.configure("mystyle.Treeview", font=('Calibri', 18), rowheight=50)
style.configure("mystyle.Treeview.Heading", font=('Calibri', 18))
tv = ttk.Treeview(tree_frame, columns=(1, 2, 3, 4, 5, 6, 7), style="mystyle.Treeview")
tv.heading("1", text="ID")
tv.column("1", width=50)
tv.heading("2", text="Name")
tv.heading("3", text="D.O.J")
tv.heading("4", text="Email")
tv.heading("5", text="Gender")
tv.heading("6", text="Contact")
tv.heading("7", text="Address")
tv['show'] = 'headings'
tv.bind("<ButtonRelease-1>", getData)
tv.pack(fill=X)

displayAll()
root.mainloop()
