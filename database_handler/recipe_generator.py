from peewee import *
from create_database import IngredientInRecipe, Recipe

database = SqliteDatabase('recipes.db')


def get_all_recipe_ids():
    query = Recipe.select(Recipe.id)
    result = [row.id for row in query]
    return result


def get_recipe_ingredients(recipe_id):
    query = (IngredientInRecipe
             .select(IngredientInRecipe.ingredient_id)
             .where(IngredientInRecipe.recipe_id == recipe_id))

    result = [row.ingredient_id for row in query]
    return result


def get_recipes_by_ingredients(ingredient_ids):
    result = []
    recipes = get_all_recipe_ids()

    for recipe_id in recipes:
        ingredients_in_recipe = get_recipe_ingredients(recipe_id)
        if all(ingredient in ingredient_ids for ingredient in ingredients_in_recipe):
            result.append(recipe_id)

    return result


list = [1, 2, 3, 4, 13, 14, 15, 16]
print(get_recipes_by_ingredients(list))
