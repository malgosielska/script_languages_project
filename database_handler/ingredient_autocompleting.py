from database_handler.create_database import Ingredient
from database_handler.constants import DATABASE

database = DATABASE


def search_ingredients_by_prefix(prefix):
    query = (Ingredient
             .select(Ingredient.name)
             .where(Ingredient.name ** f'%{prefix}%'))

    result = [row.name for row in query]

    return result
