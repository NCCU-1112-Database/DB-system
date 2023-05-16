import sqlite3

connection = sqlite3.connect('coffee.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
cur.execute("INSERT INTO Branch (Name, Address, Tel) VALUES (?, ?, ?)", ('Taipei', 'No.11 Xinglong Road.', '022387657'))
cur.execute("INSERT INTO Branch (Name, Address, Tel) VALUES (?, ?, ?)", ('Kaohsiung', 'No.22 Zhongzheng Road.', '072638148'))
cur.execute("INSERT INTO Branch (Name, Address, Tel) VALUES (?, ?, ?)", ('Tainan', 'No. 123 Mingzu Road.', '062353657'))
cur.execute("INSERT INTO Branch (Name, Address, Tel) VALUES (?, ?, ?)", ('Taoyuan', 'No. 56 Chunghua Road.', '038467657'))
cur.execute("INSERT INTO Branch (Name, Address, Tel) VALUES (?, ?, ?)", ('Taichung', 'No. 131 Keelong Road.', '042387234'))

cur.execute("INSERT INTO Producer (P_ID, Name) VALUES (?, ?)", ('101','Emart'))
cur.execute("INSERT INTO Producer (P_ID, Name) VALUES (?, ?)", ('102','Costco'))
cur.execute("INSERT INTO Producer (P_ID, Name) VALUES (?, ?)", ('103','PX'))
cur.execute("INSERT INTO Producer (P_ID, Name) VALUES (?, ?)", ('104','7-11'))
cur.execute("INSERT INTO Producer (P_ID, Name) VALUES (?, ?)", ('105','Family'))


connection.commit()
connection.close()