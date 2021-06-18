import os
import time
import datetime
import sqlite3


timing = time.time()

os.system("start python3 FR_cam_entry.py &")
os.system("start python3 FR_cam_exit.py &")
while time.time() - timing < 10.0:
    # timing = time.time()
    # print(time.time() - timing)
    a=1

# from FR_cam_exit.py import val1
#
# os.pkill(val1,0)
# print("killed")
# os.system("python3.8 Main.py")

conn1 = sqlite3.connect('Main_base.db')  # Создание основной БД
cur1 = conn1.cursor()
cur1.execute("CREATE TABLE IF NOT EXISTS users(userid INT,"
             " name TEXT, status TEXT, date dat);")  # по форме id,name,status,date
conn1.commit()

# os.system('python3.8 Main.py')

cur1.execute("SELECT * FROM users;")
for row in cur1:
    print('ID: {0} | Name: {1} | Status: {2} | Date: {3}'.format(row[0], row[1], row[2], row[3]))
one_result = cur1.fetchall()
print(one_result)

# os.system('python3.8 Main.py')
