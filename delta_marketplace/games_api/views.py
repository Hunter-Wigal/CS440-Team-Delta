from dataclasses import dataclass
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render
import mysql.connector
import json
import os


def fetch_games():
    database = mysql.connector.connect(
        host=os.environ.get("DATABASE_HOST"),
        user=os.environ.get("USER"),
        passwd=os.environ.get("PASSWORD"),
        database="delta_marketplace",
    )
    
    # cursor
    cursor = database.cursor()

    cursor.execute("""SELECT * FROM Games;""")

    contents = cursor.fetchall()

    games = []

    for row in contents:
        temp_dict = {}
        temp_dict["id"] = row[0]
        temp_dict["name"] = row[1]
        temp_dict["esrb"] = row[2]
        temp_dict["release_date"] = str(row[3])
        temp_dict["genre"] = row[4]
        temp_dict["publisher_id"] = row[5]

        games.append(temp_dict)

    to_return = {}
    to_return["games"] = games
    
    return to_return


# Create your views here.
def get_all(request: HttpRequest):

    to_return = fetch_games()

    return JsonResponse(to_return)


# Inefficiently returns games that have a matched term in the passed GET parameter
def get_games(request: HttpRequest):
    if request.method == "GET":

        # database = mysql.connector.connect(
        #     host=os.environ.get("DATABASE_HOST"),
        #     user=os.environ.get("USER"),
        #     passwd=os.environ.get("PASSWORD"),
        #     database="delta_marketplace",
        # )

        # Get the game passed to the request
        game_name = request.GET.get("g")

        # Get all games from database (should probably change to a procedure or something. wouldn't scale well with a lot of games)
        available_games = fetch_games()['games']
        
        selected_games = []
        
        game_name = game_name.lower()
        # Select only games that match the search
        for game in available_games:
            if game_name in game['name'].lower():
                selected_games.append(game)
 
                
        # print(selected_games)

        to_return = {}
        to_return['games'] = selected_games
        
        return JsonResponse(to_return)
    
    return HttpResponse("test")
