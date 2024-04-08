import mysql.connector

database = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='password'
)

# cursor
cursor = database.cursor()

# Create database
cursor.execute("CREATE DATABASE delta_marketplace")

print("Created database")