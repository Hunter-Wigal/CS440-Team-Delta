import mysql.connector
import os

database = mysql.connector.connect(
    host=os.environ.get("DATABASE_HOST"),
    user=os.environ.get("USER"),
    passwd=os.environ.get("PASSWORD"),
    database="delta_marketplace",
)

# cursor
cursor = database.cursor()

# If you get a password error, run the line below in MySQL Workbench
# ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';

# Create database
cursor.execute("CREATE DATABASE IF NOT EXISTS delta_marketplace")
