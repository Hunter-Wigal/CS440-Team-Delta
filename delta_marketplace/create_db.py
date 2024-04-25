import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

database = mysql.connector.connect(
    host=os.environ.get("DATABASE_HOST"),
    user=os.environ.get("USER"),
    passwd=os.environ.get("PASSWORD")
)

# cursor
cursor = database.cursor()

# If you get a password error, run the line below in MySQL Workbench
cursor.execute("ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';")

# Create database
cursor.execute("CREATE DATABASE IF NOT EXISTS delta_marketplace")

cursor.execute("""USE delta_marketplace;""")               
               
cursor.execute("""CREATE TABLE IF NOT EXISTS Moderators (
    mod_id INT PRIMARY KEY
);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS Publishers(
	publisher_id INT PRIMARY KEY,
    mod_id INT,
    publisher_name VARCHAR(30) UNIQUE NOT NULL,
    location VARCHAR(30),
    FOREIGN KEY (mod_id) REFERENCES Moderators(mod_id)
		ON UPDATE CASCADE
		ON DELETE RESTRICT
);""")


# esrb VARCHAR(10) DEFAULT 'PENDING',

# Changed esrb to be an int to work with the procedure for updating ratings
cursor.execute("""CREATE TABLE IF NOT EXISTS Games(
	game_id INT PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    esrb INT,
    release_date DATE NOT NULL,
    genre VARCHAR(15),
    publisher_id INT NOT NULL,
    image_url VARCHAR(30) DEFAULT '',
    description TEXT NOT NULL,
    FOREIGN KEY (publisher_id) REFERENCES Publishers(publisher_id)
		ON UPDATE CASCADE
        ON DELETE RESTRICT
);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
	username VARCHAR(30) PRIMARY KEY,
    display_name VARCHAR(30),
    full_name VARCHAR(50) NOT NULL,
    birth_date DATE NOT NULL,
    password VARCHAR(50) NOT NULL
);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS Collectibles(
	collectible_id INT PRIMARY KEY,
    game_id INT NOT NULL,
    image BLOB,
    collectible_name VARCHAR(30),
    UNIQUE(collectible_id, game_id),
    FOREIGN KEY (game_id) REFERENCES Games(game_id)
		ON UPDATE CASCADE
        ON DELETE RESTRICT
);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS GamesOwned (
    username VARCHAR(30),
    game_id INT PRIMARY KEY,
    owned_start DATE NOT NULL,
    owned_end DATE,
    FOREIGN KEY (username) REFERENCES Users (username)
		ON UPDATE CASCADE
        ON DELETE RESTRICT,
    FOREIGN KEY (game_id) REFERENCES Games (game_id)
		ON UPDATE CASCADE
        ON DELETE RESTRICT
);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS CollectiblesOwned(
	username VARCHAR(30) ,
    collectible_id INT NOT NULL,
	game_id INT NOT NULL,
    UNIQUE(collectible_id, game_id),
	PRIMARY KEY(username, collectible_id),
    FOREIGN KEY (username) REFERENCES Users(username)
		ON UPDATE CASCADE
        ON DELETE RESTRICT,
    FOREIGN KEY (collectible_id) REFERENCES Collectibles(collectible_id)
		ON UPDATE CASCADE
        ON DELETE RESTRICT,
    FOREIGN KEY (game_id) REFERENCES Games(game_id)
		ON UPDATE CASCADE
        ON DELETE RESTRICT
);""")
