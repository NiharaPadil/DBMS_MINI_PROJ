import mysql.connector

def establish_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="NiharaPadil@02022003",
        database="mini"
        
        
    )

