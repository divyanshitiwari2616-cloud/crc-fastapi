import sqlite3

connection=sqlite3.connect("sql.db")
cur=connection.cursor()
cur.execute(

"""
CREATE TABLE IF NOT EXISTS shipment(
id INTEGER,
weight REAL,
content TEXT,
status TEXT)

"""
)

#to insert data 

#cur.execute(
#"""
#INSERT INTO shipment VALUES(
#1274,
#5,
#"cpu",
#"in-transit")

#"""
#)

#to fetch data 

cur.execute(
"""
SELECT * from shipment
WHERE id=1273

"""
)

data=cur.fetchone()
print(data)


connection.commit()
connection.close()

