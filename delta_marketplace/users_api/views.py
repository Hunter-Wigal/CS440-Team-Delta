from dataclasses import dataclass
from random import randrange
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render
import mysql.connector
import json
import os
from django.views.decorators.csrf import csrf_exempt

def execute_query(query: str, values: tuple = ()):
    database = mysql.connector.connect(
        host=os.environ.get("DATABASE_HOST"),
        user=os.environ.get("USER"),
        passwd=os.environ.get("PASSWORD"),
        database="delta_marketplace",
    )
    
    # cursor
    cursor = database.cursor()

    cursor.execute(query, values)

    if "INSERT" in query:
        database.commit()
    
    contents = cursor.fetchall()
    cursor.close()
    database.close()
    
    return contents


# Fetch all user data
def fetch_user(query: str, values: tuple = ()):

    contents = execute_query(query, values)

    user = []

    for row in contents:
        temp_dict = {}
        temp_dict["username"] = row[0]
        temp_dict["dname"] = row[1]
        temp_dict["full_name"] = row[2]
        temp_dict["email"] = row[3]
        temp_dict["password"] = row[4]
        
        user.append(temp_dict)

    to_return = {}
    to_return["user"] = user

    return to_return

# Fetch games owned
def fetch_gamesOwned(query: str, values: tuple = ()):

    contents = execute_query(query, values)

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
@csrf_exempt
def user(request: HttpRequest):
    # Signing up
    if request.method == "POST":
        add_user_sql = "INSERT INTO Users (username, display_name, full_name, email, password) VALUES (%s, %s, %s, %s, %s)"
        
        username = request.POST['username']
        email = request.POST['email']
        full_name = request.POST['name']
        password = request.POST['password']
        # display_name = username

        publisher = True if request.POST['publisher'] == 'true' else False

        contents = execute_query(add_user_sql, (username, username, full_name, email, password))
        
        if publisher:
            pub_sql = "INSERT INTO Publishers (username, publisher_name, location) VALUES (%s, %s, 'TBD')"

            execute_query(pub_sql, (username, email))
        
        return HttpResponse("SUccessfully registered")
    
    # Logging in
    if request.method == "GET":
        email = request.GET['email']
        password = request.GET['password']
        
        login_query = "SELECT * FROM Users WHERE email = %s AND password = %s"
        
        contents = execute_query(login_query, (email, password))

        print(contents)
        success = len(contents) > 0
        
        if success:
            response = HttpResponse()
            response.status_code = 200
            response.content = contents[0][0]
            return response
        
        else:
            response = HttpResponse()
            response.status_code = 401
            response.content = "failed"
            return response

# Returns basic user data
def get_user(request: HttpRequest):
    if request.method == "GET":

        # Get the Username passed to the request
        user_name = request.GET.get("s")

        # Get all user data
        query = "SELECT * FROM Users WHERE username = %s;"

        # Call helper method
        results = fetch_user(query, (user_name,))

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
        query = "SELECT * FROM GamesOwned WHERE username = %s;"

        # Call helper method
        results = fetch_gamesOwned(query, (user_name,))

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
