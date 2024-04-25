from dataclasses import dataclass
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse, HttpRequest
from django.shortcuts import render
import mysql.connector
import json
import os

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

def execute_query(query: str):
    database = mysql.connector.connect(
        host=os.environ.get("DATABASE_HOST"),
        user=os.environ.get("USER"),
        passwd=os.environ.get("PASSWORD"),
        database="delta_marketplace",
    )
    
    # cursor
    cursor = database.cursor()

    cursor.execute(query)

    contents = cursor.fetchall()
    
    return contents

# Fetch games with a specific game query and return a list of dictionaries
def fetch_games(query: str):
    contents = execute_query(query)

    games = []

    for row in contents:
        temp_dict = {}
        temp_dict["id"] = row[0]
        temp_dict["name"] = row[1]
        temp_dict["esrb"] = num_to_esrb(int(row[2]))
        temp_dict["release_date"] = str(row[3])
        temp_dict["genre"] = row[4]
        temp_dict["publisher_id"] = row[5]
        temp_dict['image_url'] = row[6]

        games.append(temp_dict)

    to_return = {}
    to_return["games"] = games
    
    return to_return


# Create your views here.
def get_all(request: HttpRequest):

    to_return = fetch_games("""SELECT * FROM Games;""")

    return JsonResponse(to_return)


# Returns games that have a matched term in the passed GET parameter
def get_games(request: HttpRequest):
    if request.method == "GET":

        # Get the game passed to the request
        game_name = request.GET.get("s").lower()
        genre_choice = request.GET.get('g').lower()
        
        # Change the operator to select genres if the name isn't specified
        operator = "OR" if game_name == 'none' or genre_choice == 'none' else 'AND'

        # Get all games from database
        query  = f"SELECT * FROM Games WHERE LOWER(title) LIKE '%{game_name}%' {operator} LOWER(genre) LIKE '%{genre_choice}%';"
        
        available_games = fetch_games(query)
        
        # Check if games were actually found before indexing the dictionary
        if len(available_games) > 0:
            available_games = available_games['games']
        

        to_return = {}
        to_return['games'] = available_games
        
        return JsonResponse(to_return)
    
    return HttpResponseNotAllowed(['GET'])

# very, very insecure. Should probably use session/localstorage or something else
def get_user_games(request):
    """Returns games that are owned by the user passed as a parameter

    Args:
        request (HttpRequest): Passed automagically by django

    Returns:
        JsonResponse: The games associated with a user as json
    """    
    if request.method == "GET":
        user = request.GET.get('u')
        # Get all games from database
        query  = f"SELECT * FROM GamesOwned WHERE LOWER(username) LIKE '%{user}%';"
        
        contents = execute_query(query)

        games_owned = []

        for row in contents:
            temp_dict = {}
            temp_dict["username"] = row[0]
            temp_dict["game_id"] = row[1]
            temp_dict["owned_start"] = row[2]
            temp_dict["owned_end"] = str(row[3])

            games_owned.append(temp_dict)
        
        
        query  = "SELECT * FROM Games WHERE game_id={id};"
        game_list = []
        for game in games_owned:
            game_list.append(fetch_games(query.format(id=game['game_id']))['games'][0])
        
        to_return = {}
        to_return['games_owned'] = games_owned
        to_return['games_list'] = game_list
        
        return JsonResponse(to_return)
    
    return HttpResponseNotAllowed(['GET'])
        
# Handles actions for one game
def single_game(request: HttpRequest):
    # Return a single game
    if request.method == "GET":
        
        # Set pk to the passed game id
        pk = request.GET.get('g')
        # Define the SQL query to retrieve the game with the specified primary key
        game_query = "SELECT * FROM games WHERE game_id = {id}".format(id=pk)
        
        game = fetch_games(game_query)['games']
        
        to_return = {}
        to_return['game'] = game
        
        return JsonResponse(to_return)

    
    # Add a game
    if request.method == "POST":
        # Update this with the actual game id
        game_id = 0
        
        
        min_rating = esrb_to_num('M')
        # Call this when adding a game to ensure the rating is appropriate
        procedure_sql = "CALL UpdateESRBByGenre(%s, 'Horror', 3);" % (game_id, min_rating)
        execute_query(procedure_sql)
    
    # Update a game
    if request.method == "PUT":
        # Update this with the actual game id
        game_id = 0
        
        
        min_rating = esrb_to_num('M')
        # Call this when updating a game to make sure the rating is correct
        procedure_sql = "CALL UpdateESRBByGenre(%s, 'Horror', %s);" % (game_id, min_rating)
        execute_query(procedure_sql)

    
    # Delete a game
    if request.method == "DELETE":
        pass