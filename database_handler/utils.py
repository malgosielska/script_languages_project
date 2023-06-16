from peewee import *
from create_database import Ingredient, Recipe


def get_recipes_names():
    names = []
    recipes = Recipe.select()
    for recipe in recipes:
        names.append(recipe.name)


def get_ingredients_names():
    names = []
    ingredients = Ingredient.select()
    for ingredient in ingredients:
        names.append(ingredient.name)





