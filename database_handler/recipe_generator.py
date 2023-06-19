from database_handler.create_database import Recipe, IngredientInRecipe, Ingredient
from database_handler.constants import DATABASE

database = DATABASE


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


def get_recipes_by_ingredients(ingredient_names):
    result = []
    recipes = get_all_recipe_ids()
    ingredient_ids = get_ids_by_names(ingredient_names)
    for recipe_id in recipes:
        ingredients_in_recipe = get_recipe_ingredients(recipe_id)
        if all(ingredient in ingredient_ids for ingredient in ingredients_in_recipe):
            result.append(recipe_id)

    return get_names_by_ids(result)


def get_ids_by_names(names):
    ids = []
    ingredients = Ingredient.select().where(Ingredient.name.in_(names))
    for ingredient in ingredients:
        ids.append(ingredient.id)
    return ids


def get_names_by_ids(ids):
    names = []
    recipes = Recipe.select().where(Recipe.id.in_(ids))
    for recipe in recipes:
        names.append(recipe.name)
    return names


def get_details_by_name(name):
    try:
        recipe = Recipe.get(Recipe.name == name)
        return recipe.ingredients_desc, recipe.instructions
    except Recipe.DoesNotExist:
        return None, None
