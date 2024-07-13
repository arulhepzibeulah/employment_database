import sqlite3

class Database:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS employees(
            id INTEGER PRIMARY KEY,
            name TEXT,
            age TEXT,
            doj TEXT,
            email TEXT,
            gender TEXT,
            contact TEXT,
            address TEXT
        )
        """
        self.cur.execute(sql)
        self.con.commit()

    # Insert Function
    def insert(self, name, age, doj, email, gender, contact, address):
        
        self.cur.execute("INSERT INTO employees VALUES (NULL,?,?,?,?,?,?,?)",
                         (name, age, doj, email, gender, contact, address))
        self.con.commit()
  
    # Fetch All Data from DB
    def fetch(self):
        self.cur.execute("SELECT * from employees")
        rows=self.cur.fetchall()
        return rows

        #remove
    def remove(self,id):
         self.cur.execute(" delete from employees where id=?",(id,))             
         self.con.commit()

         #update
    def update(self,id,name, age, doj, email, gender, contact, address):
        self.cur.execute("update employees set name=?, age=?, doj=?, email=?, gender=?, contact=?, address=? where id=?",(name, age, doj, email, gender, contact, address,id))
        self.con.commit()
  
