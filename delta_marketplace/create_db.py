import mysql.connector

database = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='password'
)

# cursor
cursor = database.cursor()

# If you get a password error, run the line below in MySQL Workbench
# ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';

# Create database
cursor.execute("CREATE DATABASE IF NOT EXISTS delta_marketplace")
