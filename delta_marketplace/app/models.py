from django.db import models

# Create your models here.
class Moderators(models.Model):
    mod_id = models.IntegerField("Moderator ID", primary_key=True)

class Publishers(models.Model):
    publisher_id = models.IntegerField("Publisher ID", primary_key=True)
    mod_id = models.ForeignKey(Moderators, on_delete=models.RESTRICT, verbose_name="Moderator ID")
    pub_name = models.CharField("Publisher Name", max_length=30)
    location = models.CharField("Location", max_length=30)

class Games(models.Model):
    game_id = models.IntegerField("Game ID", primary_key=True)
    title = models.CharField("Title", max_length=50)
    esrb = models.CharField("ESRB Rating", max_length=10, default='PENDING')
    release = models.DateField("Release Date")
    genre = models.CharField("Genre", max_length=15)
    publisher_id = models.ForeignKey(Publishers, on_delete=models.RESTRICT, verbose_name="Publisher ID")

class User(models.Model):
    username = models.CharField("Username", max_length=30, primary_key=True)
    display_name = models.CharField("Display Name", max_length=30)
    full_name = models.CharField("Full Name", max_length=30)
    birth_date = models.DateField("Birth Date")

class Collectibles(models.Model):
    collectible_id = models.IntegerField("Collectible ID", primary_key=True)
    game_id = models.ForeignKey(Games, on_delete=models.RESTRICT, verbose_name="Game ID")
    image = models.ImageField("Image")
    collectible_name = models.CharField("Collectible Name", max_length=30)

# Relational Models below
class CollectiblesOwned(models.Model):
    username = models.CharField("Username", max_length=30)
    collectible_id = models.IntegerField("Collectible ID")
    game_id = models.IntegerField("Game ID")
    

class GamesOwned(models.Model):
    username = models.CharField("Username", max_length=30)
    game_id = models.IntegerField("Game ID")
    