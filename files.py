import datetime
import mysql.connector
from config import *
import csv

connection = mysql.connector.connect(
    host=BDHost,
    user=BDUser,
    passwd=BDPassword,
    port=BDPort,
    database=BDDatabase
)


cursor = connection.cursor()

# SELECT * from temp_tfg WHERE date_time BETWEEN '2020-11-09 00:00:00' AND '2020-11-09 23:59:59'

for idx in range(7):
    start = datetime.datetime(2020, 11, 9+idx)
    end = datetime.datetime(2020, 11, 9+idx, 23, 59, 59)
    my_query = "SELECT date_time, hashed_sta_eth_mac, ap_name, apiDateTime from temp_tfg WHERE date_time BETWEEN \'"+str(start)+"\' AND \'"+str(end)+"\'"
    cursor.execute(my_query)
    lines = cursor.fetchall()
    f = open("data/data_"+str(idx)+".csv", "w")
    writer = csv.writer(f)
    for i in lines:
        writer.writerow(i)
    f.close()


ap_file = open("data/ap.txt", "w")
my_query = "SELECT DISTINCT ap_name FROM temp_tfg"
cursor.execute(my_query)
aps = cursor.fetchall()

for index in aps:
    ap_file.write(str(index[0])+"\n")
ap_file.close()


if connection.is_connected():
    cursor.close()
    connection.close()
    print("MySQL cerrado")
