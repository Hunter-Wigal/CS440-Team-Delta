import mysql.connector
import datetime
from mysql.connector.errors import IntegrityError
import os

database = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='password',
)

# cursor
cursor = database.cursor()

# Drop table if exists
print("Dropping database...")
cursor.execute("""DROP DATABASE IF EXISTS delta_marketplace;""")

# os.system("python delta_marketplace\\create_db.py run")
import create_db

cursor.execute("USE delta_marketplace;")

# os.system("python delta_marketplace\\populate.py run")
import populate

print("\nInstalling requirements, please wait...\n")
os.system("\npip install -r requirements.txt\n")

print("\nFinished. Applying migrations...\n")
os.system("python delta_marketplace\\manage.py migrate")

print("\nFinished. Setting up server...\n")
os.system("python delta_marketplace\\manage.py runserver")
