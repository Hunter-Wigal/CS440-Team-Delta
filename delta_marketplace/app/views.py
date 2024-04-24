from dataclasses import dataclass
from typing import List
from django.http import HttpRequest
from django.shortcuts import redirect, render, HttpResponse
import requests
import mysql.connector
import json
import os

@dataclass
class Game:
    id: int
    name: str
    esrb: str
    release_date: str
    genre: str
    publisher_id: int
    image_url: str

@dataclass
class Publisher:
    id: int
    mod_id: int
    name: str
    location: str

@dataclass
class User:
    username: str
    display_name: str
    full_name: str
    birth_date: str

@dataclass
class Collectibles:
    id: int
    game_id: int
    image: str
    name: str

@dataclass
class GamesOwned:
    username: str
    game_id: int
    start: str
    end: str

@dataclass
class CollectiblesOwned:
    username: str
    id: int
    game_id: int

def game_resp_to_list(resp: requests.Response, games_key="games"):
    """Converts a response type from the games api to a list of game objects

    Args:
        resp (requests.Response): Response to convert
        game_key (string): the key that the games are attributed to
    Returns:
        Game: A list of game objects
    """    
    resp_dict = resp.json()
   
    games: List[Game] = []
    for item in resp_dict[games_key]:
        print(item)
        temp_game = Game(int(item['id']), item['name'], item['esrb'], item['release_date'], item['genre'], int(item['publisher_id']), item['image_url'])
        
        games.append(temp_game)
        
    return games
    
# Create your views here.
def store(request):
    resp = requests.get('http://127.0.0.1:8000/api/games/get_all')

    games = game_resp_to_list(resp)
    
    # print(games)
    return render(request, "layouts/store.html", {"games": games})

def listing(request: HttpRequest):
    return render(request, "layouts/listing.html")

def account(request: HttpRequest):
    DEBUG = bool(os.environ.get('DEBUG'))
    
    user = None
    return render(request, "layouts/account.html", {'DEBUG': DEBUG, 'user': user})

def games(request: HttpRequest):
    return render(request, "layouts/games.html")

def addUser(request: HttpRequest, userinfo = []):

    # Check for post request and parameters in the request
    if(request.method == 'POST' and len(request.POST) > 0):
        username = request.POST.get('username', 'none')
        display_name = request.POST.get('display_name', 'none')
        full_name = request.POST.get('full_name', 'none')
        birth_date = request.POST.get('birth_date', 'none')

        if username == 'none' or display_name == 'none' or full_name == 'none' or birth_date == 'none':
            userinfo = None
        else:
            userinfo = [username, display_name, full_name, birth_date]
            print(userinfo)
            # POST request to the API
            resp = requests.post

    return render(request, "layouts/addUser.html")

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


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)
  
    
def single_game_view(request: HttpRequest, pk):
    # Request the game with the passed id
    game_resp = requests.get("http://127.0.0.1:8000/api/games/game?g=%s" %(pk))
    game = game_resp_to_list(game_resp, games_key="game")[0]
    
    # Get the publisher id of the game
    pub_id = game.publisher_id
    # Get the publisher information associated with the id
    publisher_resp = requests.get("http://127.0.0.1:8000/api/publishers/publisher?p=%s" % (pub_id)).json()['publisher']
    
    # Convert the json into a publisher object
    publisher = Publisher(publisher_resp['id'], publisher_resp['mod_id'], publisher_resp['name'], publisher_resp['location'])

    
    return render(request, "layouts/game.html", {"game": game, "publisher": publisher})

def publisher_dashboard(request: HttpRequest, pk):
    
    return render(request, "layouts/publisher_dashboard.html") 

def inventory(request: HttpRequest):#, user):
    # Temporary, need a way to distinguish logged in users
    def get_curr_user():
        return "bob"
        
    user = get_curr_user()

    resp = requests.get(f'http://127.0.0.1:8000/api/games/get_user_games?u={user}')
    
    games = []
    
    # print(resp.json())
    # Check if games exist
    if len(resp.json()['games_list']) > 0:
        # print(resp.json()['games_owned'])
        games = game_resp_to_list(resp, 'games_list')
        # print(games)
    else:
        games = ['none']
        
    # print(games)
    
    return render(request, "layouts/inventory.html", {"games": games})


def users(request):
    return render(request, 'layouts/users.html')