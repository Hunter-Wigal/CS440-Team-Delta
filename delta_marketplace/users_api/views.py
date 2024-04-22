from dataclasses import dataclass
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render
import mysql.connector
import json
import os

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


# Fetch all user data
def fetch_user(query: str):

    contents = execute_query(query)

    user = []

    for row in contents:
        temp_dict = {}
        temp_dict["dname"] = row[0]
        temp_dict["full_name"] = row[1]
        temp_dict["birth_date"] = row[2]
        
        user.append(temp_dict)

    to_return = {}
    to_return["user"] = user

    return to_return

# Fetch games owned
def fetch_gamesOwned(query: str):

    contents = execute_query(query)

    gamesOwned = []

    for row in contents:
        temp_dict = {}
        temp_dict["id"] = row[0]
        temp_dict["start"] = str(row[1])
        temp_dict["end"] = str(row[2])

        gamesOwned.append(temp_dict)

    to_return = {}
    to_return["gamesOwned"] = gamesOwned
    
    return to_return

# Fetch the collectibles earned by a user
def fetch_collectiblesOwned(query: str):

    contents = execute_query(query)

    collectibles = []

    for row in contents:
        temp_dict = {}
        temp_dict["id"] = row[0]
        temp_dict["game_id"] = row[1]

        collectibles.append(temp_dict)

    to_return = {}
    to_return["collectibles"] = collectibles
    
    return to_return

# Adds a user to the database
def add_user(request: HttpRequest):
    return

# Returns basic user data
def get_user(request: HttpRequest):
    if request.method == "GET":

        # Get the Username passed to the request
        user_name = request.GET.get("s")

        # Get all user data
        query = f"SELECT * FROM Users WHERE username = '%{user_name}%';"

        # Call helper method
        results = fetch_user(query)

        # Check if the user actually has any data
        if len(results) > 0:
            results = results["user"]

        # Place the results in a dictionary and return
        to_return = {}
        to_return["user"] = results

        return JsonResponse(to_return)
    
    return HttpResponse("test")

# Returns games owned by a user
def get_owned_games(request: HttpRequest):
    if request.method == "GET":

        # Get the Username passed to the request
        user_name = request.GET.get("s")

        # Get all games for a user
        query = f"SELECT * FROM GamesOwned WHERE username = '%{user_name}%';"

        # Call helper method
        results = fetch_gamesOwned(query)

        # Check if the user actually has any games
        if len(results) > 0:
            results = results["gamesOwned"]

        # Place the results in a dictionary and return
        to_return = {}
        to_return["gamesOwned"] = results

        return JsonResponse(to_return)
    
    return HttpResponse("test")

# Returns collectibles owned by a user
def get_owned_coll(request: HttpRequest):
    if request.method == "GET":

        # Get the Username and Game ID passed to the request
        user_name = request.GET.get("s")
        game_id = request.GET.get("i")

        # Get all collectibles that a user has accrued for a specific game
        query = f"SELECT * FROM CollectiblesOwned WHERE username = '%{user_name}%' AND game_id = '{game_id}';"

        # Call helper method
        results = fetch_collectiblesOwned(query)

        # Check whether or not the user has earned any collectibles
        if len(results) > 0:
            results = results["collectiblesOwned"]

        # Place the results in a dictionary and return
        to_return = {}
        to_return["collectiblesOwned"] = results

        return JsonResponse(to_return)
    
    return HttpResponse("test")
