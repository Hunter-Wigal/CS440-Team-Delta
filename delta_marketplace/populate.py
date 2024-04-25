import mysql.connector
import datetime
from mysql.connector.errors import IntegrityError
import os
from dotenv import load_dotenv

load_dotenv()

def num_to_esrb(num):
    ratings = ['E', 'E10+', 'T', 'M', 'A', 'RP']
    if num > len(ratings):
        num = len(ratings) - 1
        
    return ratings[num]

def esrb_to_num(esrb):
    ratings = ['E', 'E10+', 'T', 'M', 'A', 'RP']
    
    if not esrb in ratings:
        return ratings.index('RP')
    
    return ratings.index(esrb)

database = mysql.connector.connect(
    host=os.environ.get("DATABASE_HOST"),
    user=os.environ.get("USER"),
    passwd=os.environ.get("PASSWORD"),
    database="delta_marketplace",
)

# cursor
cursor = database.cursor()

games_sql = "INSERT INTO Games (game_id, title, publisher_id, genre, esrb, release_date, image_url, description) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
publishers_sql = "INSERT INTO Publishers (publisher_id, username, publisher_name, location) VALUES(%s, %s, %s, %s)"
users_sql = "INSERT INTO Users(username, display_name, full_name, email, password) VALUES (%s, %s, %s, %s, %s)"
games_owned_sql = "INSERT INTO GamesOwned(username, game_id, owned_start, owned_end) VALUES (%s, %s, %s, %s)"
collectibles_squl = "INSERT INTO Collectibles(collectible_id, game_id, image_url, collectible_name) VALUES (%s, %s, %s, %s)"
collectibles_owned_sql = "INSERT INTO CollectiblesOwned(username, collectible_id, game_id) VALUES (%s, %s, %s)"

games = []
# games.append((0, "A game", datetime.date(2020, 5, 5)))
games.append((384560, 'Fun Game', 3096, 'Action', esrb_to_num('E'), datetime.date(2020,2,1), 'imgs/img.png', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'))
games.append((541513, 'COD: Fish at War ', 27376, 'FPS', esrb_to_num('M'), datetime.date(2012,11,24), 'imgs/sample2.png', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'))
games.append((985061, 'Fun Game 2', 3096, 'Adventure', esrb_to_num('T'), datetime.date(2023,4,15), 'imgs/sample3.png', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'))

collectibles = []
collectibles.append((403266, 384560, 'imgs/item1.png', 'fun item'))

publishers = []
publishers.append((27376, "user", 'Actifishion', 'Charleston, WV'))
publishers.append((3096, "bob", 'Nubisof', 'Wilmington, NC'))

users = []
users.append(("user", "real person", 'Real Person', "user@gmail.com", "temp-password"))
users.append(("bob", "real person", 'Real Person', "bob@gmail.com", "password"))

games_owned = []
games_owned.append(('bob', 384560, datetime.date(1, 1, 1), datetime.date(1, 1, 1)))

collectibles_owned = []
collectibles_owned.append(('bob', 403266, 384560))

for collectible in collectibles_owned:
    try:
        cursor.execute(collectibles_owned_sql, collectible)
    
    except IntegrityError as e:
        # Ignore just just means duplicate entry
        pass


for collectible in collectibles:
    try:
        cursor.execute(collectibles_squl, collectible)
    
    except IntegrityError as e:
        # Ignore just just means duplicate entry
        pass


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
    
for user in users:
    try:
        cursor.execute(users_sql, user)
        
    except IntegrityError as e:
        # Ignore, just just means duplicate entry
        pass
    
for game in games_owned:
    try:
        cursor.execute(games_owned_sql, game)
        
    except IntegrityError as e:
        # Ignore, just just means duplicate entry
        pass


procedure_sql = """
CREATE PROCEDURE IF NOT EXISTS UpdateESRBByGenre (
	IN p_game_id INT,
    IN p_genre VARCHAR(15),
    IN min_rating INT -- Assuming numeric values for ESRB ratings
)
BEGIN
    -- Check if the genre is 'Horror'
    IF LOWER(p_genre) = 'horror' THEN
        -- Update the ESRB rating to the maximum of the current rating and the minimum allowed rating
        UPDATE Games
        SET esrb = GREATEST(esrb, min_rating)
        WHERE game_id = p_game_id;
    -- ELSE
        -- Logic for other ratings
    END IF;
END;

"""

cursor.execute(procedure_sql)



database.commit()

cursor.close()
database.close()