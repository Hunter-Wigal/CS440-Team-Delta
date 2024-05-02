from dataclasses import dataclass
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse, HttpRequest
from django.shortcuts import render
import mysql.connector
import json
import os
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt

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

def execute_query(query: str, results=True):
    database = mysql.connector.connect(
        host=os.environ.get("DATABASE_HOST"),
        user=os.environ.get("USER"),
        passwd=os.environ.get("PASSWORD"),
        database="delta_marketplace",
    )
    
    # cursor
    cursor = database.cursor()

    cursor.execute(query)
    
    if results:
        contents = cursor.fetchall()
        
        cursor.close()
        
        return contents
    
    cursor.close()
    database.commit()
    database.close()

# Add a user to the database
def add_user(query: str):

    database = mysql.connector.connect(
        host=os.environ.get("DATABASE_HOST"),
        user=os.environ.get("USER"),
        passwd=os.environ.get("PASSWORD"),
        database="delta_marketplace",
    )




    return

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
        temp_dict['description'] = row[7]

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
        operator = "" #"OR" if game_name == 'none' or genre_choice == 'none' else 'AND'

        if game_name == 'none' or genre_choice == 'none':
            operator = "OR"
        else:
            operator = "AND"
        # Get all games from database
        query = "SELECT * FROM Games WHERE LOWER(title) LIKE '%{game}%' {operator} LOWER(genre) LIKE '%{genre}%';".format(game=game_name, operator=operator, genre=genre_choice)
        
        available_games = fetch_games(query)
        
        # Check if games were actually found before indexing the dictionary
        if len(available_games) > 0:
            available_games = available_games['games']
        

        to_return = {}
        to_return['games'] = available_games
        
        return JsonResponse(to_return)
    
    return HttpResponseNotAllowed(['GET'])

def get_publishers_games(request: HttpRequest):
    if request.method == 'GET':
        publisher_id = request.GET.get('p')
        
        try:
            publisher_id = int(publisher_id.strip('{}\'"'))
        except ValueError:
            return JsonResponse({'error': 'Invalid publisher_id'})
        
        query = f"SELECT * FROM games WHERE publisher_id = {publisher_id}"
        
        games_published = fetch_games(query)
        
        return JsonResponse(games_published)
    
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
    
    
def collectibles(request):
    if request.method == "GET":
        collectible_list = []
        id = request.GET['s']
        collectible_sql = "SELECT * FROM Collectibles WHERE collectible_id = {id}".format(id=id)
        
        contents = execute_query(collectible_sql)[0]
        
        if len(contents) > 0:
            temp_dict = {}
            temp_dict["collectible_id"] = contents[0]
            temp_dict["game_id"] = contents[1]
            temp_dict["image_url"] = contents[2]
            temp_dict["collectible_name"] = str(contents[3])
            collectible_list.append(temp_dict)
            
        to_return = {'collectible': collectible_list[0]}
        
        return JsonResponse(to_return)
        
def collectibles_owned(request):
    if request.method == "GET":
        collectibles = []
        username = request.GET['u']
        collectible_sql = "SELECT * FROM CollectiblesOwned WHERE username = '{user}'".format(user=username)
        
        contents = execute_query(collectible_sql)

        for row in contents:
            temp_dict = {}
            temp_dict["username"] = row[0]
            temp_dict["collectible_id"] = row[1]
            temp_dict["game_id"] = row[2]

            collectibles.append(temp_dict)
            
        to_return = {}
        to_return['collectibles'] = collectibles
        return JsonResponse(to_return)
    
@csrf_exempt
def purchase(request: HttpRequest):
    if request.method == "POST":
        userID = request.POST["u"]
        gameID = request.POST["g"]
        
        # Purchasing or renting
        type = request.POST["t"]
        
        owned_start = datetime.today().date()
        owned_end = datetime(2100, 1, 1).date()
        if type != "buy":
            owned_end = owned_start + timedelta(30)
        
        purchase_sql = "INSERT INTO GamesOwned(username, game_id, owned_start, owned_end) VALUES ('%s', '%s', '%s', '%s');" % (userID, gameID, owned_start, owned_end)
        print(purchase_sql)
        execute_query(purchase_sql, False)
        
        response = HttpResponse()
        response.status_code = 200
        return response
    
    response = HttpResponse()
    response.status_code = 401
    return response