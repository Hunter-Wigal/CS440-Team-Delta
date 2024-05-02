from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
import os
import random
from django.urls import reverse
import mysql.connector
import requests


def esrb_to_num(esrb):
    ratings = ['E', 'E10+', 'T', 'M', 'A', 'RP']
    
    if not esrb in ratings:
        return ratings.index('RP')
    
    return ratings.index(esrb)

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

    contents = cursor.fetchall()
    
    cursor.close()
    database.close()
    
    return contents

def add_game(request: HttpRequest):
    if request.method == 'POST':
        # Parse data into variables
        title = request.POST['name']
        description = request.POST['description']
        esrb = esrb_to_num(request.POST['esrb'])
        release_date = request.POST['date']
        genre = request.POST['genre']
        image_url = request.POST['image']
        
        # TODO could probably use better error handling. Assume the user has to be logged in I guess
        username = request.COOKIES['username']
        # TODO Api call in the same api. Yes there are probably better ways
        pub_resp = requests.get(f"http://127.0.0.1:8000/api/publishers/publisher?p={username}").json()
        publisher_id = pub_resp['publisher']['id']
        
        try:
            #Establish connection to DB
            database = mysql.connector.connect(
                host= os.environ.get("DATABASE_HOST"),
                user=os.environ.get("USER"),
                passwd=os.environ.get("PASSWORD"),
                database="delta_marketplace"
            )
            cursor = database.cursor()
            
            insert_query = "INSERT INTO Games (title, esrb, release_date, genre, publisher_id, image_url, description) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (title, esrb, release_date, genre, publisher_id, image_url, description)
            cursor.execute(insert_query, values)
            
            
            min_rating = esrb_to_num('M')
            # Call this when adding a game to make sure the rating is correct
            # procedure_sql = "CALL UpdateESRBByGenre(%s, 'Horror', %s);" % (game_id, min_rating)
            # execute_query(procedure_sql)
            
            database.commit()
            
            cursor.close()
            
            print("Successfully added game into database!")
            # Temporary fix. Using username instead of id
            publisher_id = request.COOKIES['username']
            return redirect('publisher_dashboard', pk=publisher_id)
        
        except mysql.connector.Error as err:
            return HttpResponse(f"Error: {err}")
        
def update_game(request: HttpRequest):
    if request.method == 'POST':
        # Parse data into variables
        game_id = request.POST['game_id']
        title = request.POST['name']
        description = request.POST['description']
        esrb = esrb_to_num(request.POST['esrb'])
        release_date = request.POST['date']
        genre = request.POST['genre']
        image_url = request.POST['image']
        publisher_id = request.POST['publisher_id']
        
        try:
            #Establish connection to DB
            database = mysql.connector.connect(
                host= os.environ.get("DATABASE_HOST"),
                user=os.environ.get("USER"),
                passwd=os.environ.get("PASSWORD"),
                database="delta_marketplace"
            )
            cursor = database.cursor()
            
            update_query = """
                UPDATE Games 
                SET title = %s, esrb = %s, release_date = %s, 
                genre = %s, publisher_id = %s, image_url = %s, 
                description = %s 
                WHERE game_id = %s
            """
            values = (title, esrb, release_date, genre, publisher_id, image_url, description, game_id)
            cursor.execute(update_query, values)
            
            database.commit()
            
            cursor.close()
            
            print("Successfully updated game into database!")
            
            # Temporary fix. Using username instead of id
            publisher_id = request.COOKIES['username']
            return redirect('publisher_dashboard', pk=publisher_id)
        
        except mysql.connector.Error as err:
            return HttpResponse(f"Error: {err}")

def remove_game(request: HttpRequest):
    if request.method == 'POST':
        game_id = request.POST.get('game_id')
        publisher_id = request.POST.get('publisher_id')
        
        try:
             #Establish connection to DB
            database = mysql.connector.connect(
                host= os.environ.get("DATABASE_HOST"),
                user=os.environ.get("USER"),
                passwd=os.environ.get("PASSWORD"),
                database="delta_marketplace"
            )
            cursor = database.cursor()
            delete_query = "DELETE FROM games WHERE game_id = %s"
            cursor.execute(delete_query, [game_id])
            database.commit()
            cursor.close()
                
        except Exception as e:
            return JsonResponse({'error': str(e)} , status=500)

        # Temporary fix. Using username instead of id
        publisher_id = request.COOKIES['username']
        return redirect('publisher_dashboard', publisher_id)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def publisher(request: HttpRequest):
    if request.method == "GET":
        # Set publisher to the passed publisher id
        pub = request.GET.get('p')
        print(request.GET.get('i'))
        column_name = "username"
        if request.GET.get('i') != None:
            column_name = "publisher_id"
        
        publisher_query = "SELECT * FROM publishers WHERE {column} = '{id}'".format(id=pub, column=column_name)

        publisher_result = execute_query(publisher_query)
        
        new_query = "SELECT * FROM publishers, users WHERE publishers.username = users.username AND users.username = %s;"
        
        to_return = {}
        # Format with user information as well as publisher info
        if request.GET.get('i') == None:
            if len(publisher_result) > 0:
                publisher_result = execute_query(new_query, (pub,))
                print(publisher_result)
                
                publisher_result = publisher_result[0]
                publisher = {}
                publisher["id"] = publisher_result[0]
                publisher["username"] = publisher_result[1]
                publisher["name"] = publisher_result[2]
                publisher["location"] = publisher_result[3]
                
                publisher["full_name"] = publisher_result[6]
                publisher["email"] = publisher_result[7]
                
                print(publisher)
                to_return['publisher'] = publisher
                return JsonResponse(to_return)
        
        # print(result)
 
        
        if len(publisher_result) > 0:
            publisher_result = publisher_result[0]
            publisher = {}
            publisher["id"] = publisher_result[0]
            publisher["username"] = publisher_result[1]
            publisher["name"] = publisher_result[2]
            publisher["location"] = publisher_result[3]
            
            to_return['publisher'] = publisher
            
        else:
            to_return = {'publisher': 'none'}
        
        return JsonResponse(to_return)