import sqlite3

con = sqlite3.connect("test.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, name TEXT)")
cur.execute("INSERT INTO test (name) VALUES ('hello world')")

con.commit()

cur.execute("SELECT * FROM test")
print(cur.fetchall())
