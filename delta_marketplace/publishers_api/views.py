from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
import os
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