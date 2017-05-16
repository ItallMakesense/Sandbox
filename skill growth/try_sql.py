import sqlite3
import os

conn = sqlite3.connect(os.getcwd() + '/example.db')
c = conn.cursor()
c.execute('''CREATE TABLE stocks
             (date text, trans text, symbol text, qty real, price real)''')
c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
conn.commit()
t = ('RHAT',)
c.execute('SELECT * FROM stocks WHERE symbol=?', t)
print(c.fetchone())
conn.close()