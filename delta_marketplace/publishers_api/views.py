from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
import os
import random
import mysql.connector

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
        esrb = request.POST['esrb']
        release_date = request.POST['date']
        genre = request.POST['genre']
        image_url = request.POST['image']
        
        # Currently using an RNG need to change this to what we want to do.
        game_id = random.randint(1, 100)
        
        try:
            #Establish connection to DB
            database = mysql.connector.connect(
                host= os.environ.get("DATABASE_HOST"),
                user=os.environ.get("USER"),
                passwd=os.environ.get("PASSWORD"),
                database="delta_marketplace"
            )
            cursor = database.cursor()
            
            insert_query = "INSERT INTO Games (game_id, title, esrb, release_date, genre, publisher_id, image_url, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            values = (game_id, title, esrb, release_date, genre, 3096, image_url, description)
            cursor.execute(insert_query, values)
            
            database.commit()
            
            cursor.close()
            
            return redirect('publisher_dashboard')
        
        except mysql.connector.Error as err:
            return HttpResponse(f"Error: {err}")


# Create your views here.
def publisher(request: HttpRequest):
    if request.method == "GET":
        
        # Set publisher to the passed publisher id
        pub = request.GET.get('p')
        publisher_query = "SELECT * FROM publishers WHERE publisher_id = {id}".format(id=pub)

        publisher_result = execute_query(publisher_query)[0]
        
        publisher = {}
        publisher["id"] = publisher_result[0]
        publisher["mod_id"] = publisher_result[1]
        publisher["name"] = publisher_result[2]
        publisher["location"] = publisher_result[3]
        
        to_return = {}
        to_return['publisher'] = publisher
        
        return JsonResponse(to_return)