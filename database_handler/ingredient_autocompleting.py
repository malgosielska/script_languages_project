import re
from peewee import *

from database_handler.create_database import Ingredient

database = SqliteDatabase('../database_handler/recipes.db')


def search_ingredients_by_prefix(prefix):
    # Tworzenie zapytania do bazy danych
    query = (Ingredient
             .select(Ingredient.name)
             .where(Ingredient.name ** f'%{prefix}%'))

    # Wykonanie zapytania i pobranie wyników
    result = [row.name for row in query]

    return result


prefix = "cheese"
ingredients = search_ingredients_by_prefix(prefix)
print(ingredients)
