import sqlite3

conn = sqlite3.connect("quiz.db")

with open("questions.sql","r") as f:
    sql = f.read()

conn.executescript(sql)

conn.commit()
conn.close()

print("Questions Imported Successfully")