from dataclasses import dataclass
from typing import List
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect, render, HttpResponse
from django.views.generic.edit import FormView
from django import forms
import requests
import json
import os
from django.template import RequestContext

user = None
@dataclass
class Game:
    id: int
    name: str
    esrb: str
    release_date: str
    genre: str
    publisher_id: int
    image_url: str
    description: str


@dataclass
class Publisher:
    id: int
    username: str
    name: str
    location: str


@dataclass
class User:
    username: str
    display_name: str
    full_name: str
    email: str


@dataclass
class Collectible:
    id: int
    game_id: int
    image_url: str
    name: str


@dataclass
class GamesOwned:
    username: str
    game_id: int
    start: str
    end: str


@dataclass
class CollectiblesOwned:
    username: str
    id: int
    game_id: int
    
def get_user(username: str):
    resp = requests.get(
        "http://127.0.0.1:8000/api/users/get_user?s={username}".format(
            username=username
        )
    )
    user = None
    if len(resp.json()["user"]) < 1:
        # TODO reformat this
        user = None
    # Assume the user was found
    else:
        json = resp.json()["user"][0]
        user = User(
            json["username"], json["dname"], json["full_name"], json["email"]
        )

    return user

# Decorator for adding a user to the request. Used specifically for the navbar
def add_user(func):
    # added arguments inside the inner1,
    # if function takes any arguments,
    # can be added like this.
    def inner1(*args, **kwargs):
        request: HttpRequest = args[0]
        user = None

        if "username" in request.COOKIES.keys():
            username = request.COOKIES["username"]
            user = get_user(username)
            
        return_val = func(*args, **kwargs, user=user)
        return return_val

    return inner1


def game_resp_to_list(resp: requests.Response, games_key="games"):
    """Converts a response type from the games api to a list of game objects

    Args:
        resp (requests.Response): Response to convert
        game_key (string): the key that the games are attributed to
    Returns:
        Game: A list of game objects
    """
    resp_dict = resp.json()

    games: List[Game] = []
    for item in resp_dict[games_key]:
        temp_game = Game(
            int(item["id"]),
            item["name"],
            item["esrb"],
            item["release_date"],
            item["genre"],
            int(item["publisher_id"]),
            item["image_url"],
            item["description"],
        )

        games.append(temp_game)

    return games


class SignupForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30)
    display_name = forms.CharField(label="Display Name", max_length=30)
    full_name = forms.CharField(label="Full Name", max_length=50)
    email = forms.EmailField(label="Email", max_length=50)
    password = forms.CharField(
        label="Password", max_length=50, widget=forms.PasswordInput
    )


def create_account(request: HttpRequest):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            display_name = form.cleaned_data["dname"]
            full_name = form.cleaned_data["full_name"]
            email = form.cleaned_data["email"]
            passwd = form.cleaned_data["password"]

            user = User(username, display_name, full_name, email, passwd)

            # Send the user to the users api
            resp = requests.post("", {"form": form})

    else:
        form = SignupForm()
        return render(request, "base.html", {"form": form})


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(
        label="Password", max_length=50, widget=forms.PasswordInput
    )


@add_user
def store(request: HttpRequest, user=None):
    resp = requests.get("http://127.0.0.1:8000/api/games/get_all")

    games = game_resp_to_list(resp)

    return render(request, "layouts/store.html", context={"games": games, "user": user})

@add_user
def listing(request: HttpRequest, user=None):
    return render(request, "layouts/listing.html", {"user": user})

@add_user
def account(request: HttpRequest, user=None):
    DEBUG = True  # bool(os.environ.get('DEBUG'))
    username = request.COOKIES["username"]

    resp = requests.get(
        "http://127.0.0.1:8000/api/users/get_user?s={username}".format(
            username=username
        )
    )

    user = None
    if len(resp.json()["user"]) < 1:
        # TODO reformat this
        user = None
    # Assume the user was found
    else:
        json = resp.json()["user"][0]
        user = User(json["username"], json["dname"], json["full_name"], json["email"])

    return render(request, "layouts/account.html", {"DEBUG": DEBUG, "user": user})

@add_user
def games(request: HttpRequest, user=None):
    return render(request, "layouts/games.html", {"user": user})

@add_user
def addUser(request: HttpRequest, userinfo=[], user=None):

    # Check for post request and parameters in the request
    if request.method == "POST" and len(request.POST) > 0:
        username = request.POST.get("username", "none")
        display_name = request.POST.get("display_name", "none")
        full_name = request.POST.get("full_name", "none")
        birth_date = request.POST.get("birth_date", "none")

        if (
            username == "none"
            or display_name == "none"
            or full_name == "none"
            or birth_date == "none"
        ):
            userinfo = None
        else:
            userinfo = [username, display_name, full_name, birth_date]
            # POST request to the API
            # resp = requests.post

    return render(request, "layouts/addUser.html")

@add_user
def search(request: HttpRequest, search_results=[], user=None):

    # Check for get request and parameters in the request
    if request.method == "GET" and len(request.GET) > 0:
        to_search = request.GET.get("gamesearch", "none")
        genre = request.GET.get("genre", "none")

        if to_search == "":
            to_search = "none"

        resp = requests.get(
            "http://127.0.0.1:8000/api/games/get_games?s=%s&g=%s" % (to_search, genre)
        )
        search_results = game_resp_to_list(resp)

        if len(search_results) < 1:
            search_results = None
            print("No results found")

        # Search can't be an empty string
        if len(to_search) < 1 and genre == "none":
            search_results = None

    return render(request, "layouts/search.html", {"results": search_results, "user": user})


def custom_404_view(request, exception):
    return render(request, "404.html", status=404)

@add_user
def single_game_view(request: HttpRequest, pk, user=None):
    # Request the game with the passed id
    game_resp = requests.get("http://127.0.0.1:8000/api/games/game?g=%s" % (pk))
    game = game_resp_to_list(game_resp, games_key="game")[0]

    # Get the publisher id of the game
    pub_id = game.publisher_id
    # Get the publisher information associated with the id
    publisher_resp = requests.get(
        "http://127.0.0.1:8000/api/publishers/publisher?p=%s" % (pub_id)
    ).json()["publisher"]

    # Convert the json into a publisher object
    publisher = Publisher(
        publisher_resp["id"],
        publisher_resp["username"],
        publisher_resp["name"],
        publisher_resp["location"],
    )

    return render(request, "layouts/game.html", {"game": game, "publisher": publisher, "user": user})

@add_user
def publisher_dashboard(request: HttpRequest, pk, user=None):
    # Get the publisher id of the game
    pub_id = pk
    # Get the publisher information associated with the id
    publisher_resp = requests.get(
        "http://127.0.0.1:8000/api/publishers/publisher?p=%s" % (pub_id)
    ).json()["publisher"]
    publisher = Publisher(
        publisher_resp["id"],
        publisher_resp["username"],
        publisher_resp["name"],
        publisher_resp["location"],
    )

    games_published_resp = requests.get(
        "http://127.0.0.1:8000/api/games/get_publishers_games?p=%s" % {pk}
    )
    games_published = game_resp_to_list(games_published_resp)

    return render(
        request,
        "layouts/publisher_dashboard.html",
        {"games_published": games_published, "publisher": publisher, "user": user},
    )

@add_user
def add_game_view(request: HttpRequest, user=None):
    return render(request, "layouts/add_game.html", {"user": user})

@add_user
def edit_game_view(request: HttpRequest, pk, user=None):

    # Request the game with the passed id
    game_resp = requests.get("http://127.0.0.1:8000/api/games/game?g=%s" % (pk))
    game = game_resp_to_list(game_resp, games_key="game")[0]

    return render(request, "layouts/edit_game.html", {"game": game, "user": user})

@add_user
def inventory(request: HttpRequest, user=None):
    username = user.username

    resp = requests.get(f"http://127.0.0.1:8000/api/games/get_user_games?u={username}")

    games = []

    # Check if games exist
    if len(resp.json()["games_list"]) > 0:
        games = game_resp_to_list(resp, "games_list")
    else:
        games = ["none"]

    collectibles = []

    resp = requests.get(
        f"http://127.0.0.1:8000/api/games/collectibles_owned?u={username}"
    ).json()

    for collectible_owned in resp["collectibles"]:
        collectible_id = collectible_owned["collectible_id"]
        collectible_found = requests.get(
            f"http://127.0.0.1:8000/api/games/collectibles?s={collectible_id}"
        ).json()["collectible"]
        collectible = Collectible(
            collectible_found["collectible_id"],
            collectible_found["game_id"],
            collectible_found["image_url"],
            collectible_found["collectible_name"].capitalize(),
        )
        collectibles.append(collectible)

    return render(
        request,
        "layouts/inventory.html",
        {"games": games, "collectibles": collectibles, "user": user},
    )


# def users(request):
#     return render(request, 'layouts/users.html')

def logout(request: HttpRequest):

    response = HttpResponseRedirect('/')
    response.delete_cookie('username')
    return response
