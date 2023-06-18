from peewee import *

from database_handler.create_database import Ingredient

database = SqliteDatabase('../database_handler/recipes.db')


def search_ingredients_by_prefix(prefix):
    # query to the database
    query = (Ingredient
             .select(Ingredient.name)
             .where(Ingredient.name ** f'%{prefix}%'))

    result = [row.name for row in query]

    return result
