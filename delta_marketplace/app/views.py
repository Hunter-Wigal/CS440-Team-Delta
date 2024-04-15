from dataclasses import dataclass
from typing import List
from django.shortcuts import render, HttpResponse
import requests

@dataclass
class Game:
    id: int
    name: str
    esrb: str
    release_date: str
    genre: str
    publisher_id: int
    
# Create your views here.
def store(request):
    games: List[Game] = []

    resp = requests.get('http://127.0.0.1:8000/api/games/get_all')
    resp_dict = resp.json()
   
    for item in resp_dict['games']:
        temp_game = Game(int(item['id']), item['name'], item['esrb'], item['release_date'], item['genre'], int(item['publisher_id']))
        
        games.append(temp_game)
    
    # print(games)
    return render(request, "layouts/store.html", {"games": games})

def listing(request):
    return render(request, "layouts/listing.html")

def user(request):
    return render(request, "layouts/user.html")