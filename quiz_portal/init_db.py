import sqlite3

conn = sqlite3.connect("quiz.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT UNIQUE,
password TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS questions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
question TEXT,
option1 TEXT,
option2 TEXT,
option3 TEXT,
option4 TEXT,
answer TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS results(
id INTEGER PRIMARY KEY AUTOINCREMENT,
email TEXT,
score REAL,
percentage INTEGER,
date TEXT
)
""")

conn.commit()
conn.close()

print("Database Created")