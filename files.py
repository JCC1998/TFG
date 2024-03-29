import datetime
import mysql.connector
from config import *
import csv
from tqdm import tqdm


def create_data_files(year, month, day, sample_days):
    # Establecemos una conexión con la base de datos
    connection = mysql.connector.connect(
        host=BDHost,
        user=BDUser,
        passwd=BDPassword,
        port=BDPort,
        database=BDDatabase
    )

    if not connection.is_connected():
        print("No se ha podido establecer una comunicación con la base de datos")
    cursor = connection.cursor()

    # SELECT * from temp_tfg WHERE date_time BETWEEN '2020-11-09 00:00:00' AND '2020-11-09 23:59:59'
    for idx in tqdm(range(sample_days)):
        start = datetime.datetime(year, month, day + idx)
        end = datetime.datetime(year, month, day + idx, 23, 59, 59)
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
