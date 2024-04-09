import mysql.connector

database = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='password',
    database='delta_marketplace'
)

# cursor
cursor = database.cursor()

cursor.execute('CREATE TABLE test('
    'testID INT PRIMARY KEY,'
    'testString VARCHAR(20)'
    ')')

cursor.execute("INSERT INTO test VALUES(0, 'A string')")

database.commit()

cursor.close()
database.close()