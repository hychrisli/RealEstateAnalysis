import mysql.connector

config = {
    'user': 'mlsuser',
    'password': 'mls123',
    'host': '192.168.0.252'}

cnx = mysql.connector.connect(** config)
cnx.close()