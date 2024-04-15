from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import mysql.connector
import json

# Create your views here.
def get_all(request):
    
    # Move this into a get request
    database = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='password',
        database='delta_marketplace'
    )
    # cursor
    cursor = database.cursor()

    cursor.execute("""SELECT * FROM Games;""")
    
    contents = cursor.fetchall()
    print(type(contents))
    
    games = []
    
    #id, name, esrb, release_date, genre, publisher_id
    #(384560, 'Fun Game', 'E', datetime.date(2020, 2, 1), 'Action', 3096)
    
    for row in contents:
        temp_dict = {}
        temp_dict['id'] = row[0]
        temp_dict['name'] = row[1]
        temp_dict['esrb'] = row[2]
        temp_dict['release_date'] = str(row[3])
        temp_dict['genre'] = row[4]
        temp_dict['publisher_id'] = row[5]
        print(temp_dict)
        
        games.append(temp_dict)
    
    to_return = {}
    to_return['games'] = games
    
    return JsonResponse(to_return)