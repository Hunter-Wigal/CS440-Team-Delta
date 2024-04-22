from dataclasses import dataclass
from typing import List
from django.http import HttpRequest
from django.shortcuts import redirect, render, HttpResponse
import requests


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

def games(request):
    return render(request, "layouts/games.html")


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

def inventory(request):
    return render(request, "layouts/inventory.html")