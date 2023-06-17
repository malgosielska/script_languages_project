from peewee import *

from database_handler.create_database import Recipe, Ingredient, IngredientInRecipe


def get_recipes_names():
    names = []
    recipes = Recipe.select()
    for recipe in recipes:
        names.append(recipe.name)
    return names


def get_ingredients_names():
    names = []
    ingredients = Ingredient.select()
    for ingredient in ingredients:
        names.append(ingredient.name)
    return names
