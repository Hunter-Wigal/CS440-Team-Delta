import mysql.connector
import datetime
from mysql.connector.errors import IntegrityError


database = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='password',
    database='delta_marketplace'
)

# cursor
cursor = database.cursor()

games_sql = "INSERT INTO Games (game_id, title, publisher_id, genre, esrb, release_date) VALUES(%s, %s, %s, %s, %s, %s)"
publishers_sql = "INSERT INTO Publishers (publisher_id, publisher_name, location) VALUES(%s, %s, %s)"

games = []
# games.append((0, "A game", datetime.date(2020, 5, 5)))
games.append((384560, 'Fun Game', 3096, 'Action', 'E', datetime.date(2020,2,1)))
games.append((541513, 'COD: Fish at War ', 27376, 'FPS', 'M', datetime.date(2012,11,24)))
games.append((985061, 'Fun Game 2', 3096, 'Adventure', 'T', datetime.date(2023,4,15)))

publishers = []
publishers.append((27376, 'Actifishion', 'Charleston, WV'))
publishers.append((3096, 'Nubisof', 'Wilmington, NC'))

for publisher in publishers:
    try:
        cursor.execute(publishers_sql, publisher)
        
    except IntegrityError as e:
        # Ignore, just just means duplicate entry
        pass


for game in games:
    try:
        cursor.execute(games_sql, game)
        
    except IntegrityError as e:
        # Ignore, just just means duplicate entry
        pass



database.commit()

cursor.close()
database.close()