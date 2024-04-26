from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
import os
import random
from django.urls import reverse
import mysql.connector


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

def add_game(request: HttpRequest):
    if request.method == 'POST':
        # Parse data into variables
        title = request.POST['name']
        description = request.POST['description']
        esrb = esrb_to_num(request.POST['esrb'])
        release_date = request.POST['date']
        genre = request.POST['genre']
        image_url = request.POST['image']
        publisher_id = 3096
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
            
            database.commit()
            
            cursor.close()
            
            print("Successfully added game into database!")
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
            return redirect('publisher_dashboard', pk=publisher_id)
        
        except mysql.connector.Error as err:
            return HttpResponse(f"Error: {err}")

def remove_game(request: HttpRequest):
    if request.method == 'POST':
        game_id = request.POST.get('game_id')
        publisher_id = request.POST.get('publisher_id')
        print("This is the publisher_id:", publisher_id)
        
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

        return redirect('publisher_dashboard', publisher_id)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# Create your views here.
def publisher(request: HttpRequest):
    if request.method == "GET":
        
        # Set publisher to the passed publisher id
        pub = request.GET.get('p')
        publisher_query = "SELECT * FROM publishers WHERE publisher_id = {id}".format(id=pub)

        publisher_result = execute_query(publisher_query)[0]
        
        publisher = {}
        publisher["id"] = publisher_result[0]
        publisher["username"] = publisher_result[1]
        publisher["name"] = publisher_result[2]
        publisher["location"] = publisher_result[3]
        
        to_return = {}
        to_return['publisher'] = publisher
        
        return JsonResponse(to_return)