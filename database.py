import sqlite3


class Database:
    def __init__(self, db):
        """
        The function creates a table called students in the database if it doesn't already exist
        
        :param db: The name of the database file
        """
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS students (id TEXT PRIMARY KEY, name TEXT, image BLOB, face_encoding BLOB);"
        )
        self.conn.commit()

    def fetch(self):
        """
        It fetches all the rows from the students table and returns them as a list of tuples
        :return: The fetchall() method returns all the rows in the table.
        """
        self.cur.execute("SELECT * FROM students;")
        return self.cur.fetchall()
    
    def fetch_id_and_name(self):
        """
        It fetches the id and name column all the rows from the students table and returns a list of tuples
        :return: A list of tuples.
        """
        self.cur.execute("SELECT id, name FROM students;")
        return self.cur.fetchall()

    def insert(self, id, name, image, face_encoding):
        """
        It takes in the id, name, image, and face_encoding of a student and inserts it into the database
        
        :param id: The id of the student
        :param name: The name of the student
        :param image: the image of the student
        :param face_encoding: A numpy array of 128 numbers that describe the face in image
        """
        self.cur.execute(
            "INSERT INTO students VALUES (?, ?, ?, ?);",
            (id, name, image, face_encoding),
        )
        self.conn.commit()

    def remove(self, id):
        """
        It deletes a student from the database
        
        :param id: The id of the student to be removed
        """
        self.cur.execute("DELETE FROM students WHERE id=?", (id,))
        self.conn.commit()

    def update_name(self, id, name):
        """
        It updates the name of a student in the database
        
        :param id: The id of the student to update
        :param name: New name for the student
        """
        self.cur.execute(
            "UPDATE students SET name = ? WHERE id = ?",
            (name, id),
        )
        self.conn.commit()

    def __del__(self):
        self.conn.close()
