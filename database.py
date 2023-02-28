import sqlite3


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS students (id TEXT PRIMARY KEY, name TEXT, image BLOB, face_encoding BLOB);"
        )
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM students;")
        return self.cur.fetchall()
    
    def fetch_id_and_name(self):
        self.cur.execute("SELECT id, name FROM students;")
        return self.cur.fetchall()

    def insert(self, id, name, image, face_encoding):
        self.cur.execute(
            "INSERT INTO students VALUES (?, ?, ?, ?);",
            (id, name, image, face_encoding),
        )
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM students WHERE id=?", (id,))
        self.conn.commit()

    # def update(self, id, part, customer, retailer, price):
    #     self.cur.execute(
    #         "UPDATE parts SET part = ?, customer = ?, retailer = ?, price = ? WHERE id = ?",
    #         (part, customer, retailer, price, id),
    #     )
    #     self.conn.commit()

    def __del__(self):
        self.conn.close()
