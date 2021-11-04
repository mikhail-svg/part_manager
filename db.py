import sqlite3


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, student_name text, student_age text, homeroom_teacher text, avg_grade text)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM students")
        rows = self.cur.fetchall()
        return rows

    def insert(self, student_name, student_age, homeroom_teacher, avg_grade):
        self.cur.execute("INSERT INTO students VALUES (NULL, ?, ?, ?, ?)",
                         (student_name, student_age, homeroom_teacher, avg_grade))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM students WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, student_name, student_age, homeroom_teacher, avg_grade):
        self.cur.execute("UPDATE students SET part = ?, customer = ?, retailer = ?, price = ? WHERE id = ?",
                         (student_name, student_age, homeroom_teacher, avg_grade, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()


db = Database('students.db')

