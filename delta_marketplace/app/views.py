from dataclasses import dataclass
from typing import List
from django.http import HttpRequest
from django.shortcuts import redirect, render, HttpResponse
import requests
import mysql.connector
import os


@dataclass
class Game:
    id: int
    name: str
    esrb: str
    release_date: str
    genre: str
    publisher_id: int
    

def game_resp_to_list(resp: requests.Response):
    """Converts a response type from the games api to a list of game objects

    Args:
        resp (requests.Response): Response to convert

    Returns:
        games: A list of game objects
    """    
    resp_dict = resp.json()
   
    games: List[Game] = []
    for item in resp_dict['games']:
        temp_game = Game(int(item['id']), item['name'], item['esrb'], item['release_date'], item['genre'], int(item['publisher_id']))
        
        games.append(temp_game)
        
    return games
    
# Create your views here.
def store(request):
    resp = requests.get('http://127.0.0.1:8000/api/games/get_all')

    games = game_resp_to_list(resp)
    
    # print(games)
    return render(request, "layouts/store.html", {"games": games})

def listing(request):
    return render(request, "layouts/listing.html")

def account(request):
    return render(request, "layouts/account.html")


def search(request: HttpRequest, search_results=[]):
    
    # Check for get request and parameters in the request
    if(request.method == 'GET' and len(request.GET) > 0):
        to_search = request.GET.get('gamesearch', 'none')
        genre = request.GET.get('genre', 'none')
        
        if to_search == '':
            to_search = 'none'
            
        resp = requests.get('http://127.0.0.1:8000/api/games/get_games?s=%s&g=%s' % (to_search, genre))
        search_results = game_resp_to_list(resp)
        # print('http://127.0.0.1:8000/api/games/get_games?g=%s' % to_search)

        if len(search_results) < 1:
            search_results = None
            print("No results found")

        # Search can't be an empty string
        if(len(to_search) < 1 and genre == 'none'):
            search_results = None

        

    return render(request, 'layouts/search.html', {'results': search_results})

def execute_single_game_query(query: str):
    database = mysql.connector.connect(
        host=os.environ.get("DATABASE_HOST"),
        user=os.environ.get("USER"),
        passwd=os.environ.get("PASSWORD"),
        database="delta_marketplace",
    )

    # cursor
    cursor = database.cursor()

    

def single_game_view(request: HttpRequest, pk):
    database = mysql.connector.connect(
        host=os.environ.get("DATABASE_HOST"),
        user=os.environ.get("USER"),
        passwd=os.environ.get("PASSWORD"),
        database="delta_marketplace",
    )
    # Define the SQL query to retrieve the game with the specified primary key
    game_query = "SELECT * FROM games WHERE game_id = %s"
    publisher_query = "SELECT * FROM publishers WHERE publisher_id = %s"

    # Execute the SQL query with the primary key as parameter
    with database.cursor() as cursor:
        cursor.execute(game_query, [pk])
        result = cursor.fetchone()  
     
    game = {}  
 
    game["id"] = result[0]
    game["name"] = result[1]
    game["esrb"] = result[2]
    game["release_date"] = str(result[3])
    game["genre"] = result[4]
    game["publisher_id"] = result[5]
    
    with database.cursor() as cursor:
        cursor.execute(publisher_query, [game["publisher_id"]])
        result = cursor.fetchone()
    
    publisher = {}
    publisher["id"] = result[0]
    publisher["mod_id"] = result[1]
    publisher["name"] = result[2]
    publisher["location"] = result[3]
    
    return render(request, "layouts/game.html", {"game": game, "publisher": publisher}) 

def inventory(request):
    return render(request, "layouts/inventory.html")