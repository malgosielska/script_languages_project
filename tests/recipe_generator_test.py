import pytest
from peewee import SqliteDatabase
from database_handler.create_database import Ingredient, Recipe, IngredientInRecipe
from database_handler.recipe_generator import get_all_recipe_ids, get_recipe_ingredients, \
    get_recipes_by_ingredients, get_ids_by_names, get_names_by_ids, get_details_by_name


@pytest.fixture(scope="function")
def test_database():
    # Create an in-memory SQLite database for testing
    database = SqliteDatabase(':memory:')
    database.bind([Ingredient, Recipe, IngredientInRecipe])
    database.connect()
    database.create_tables([Ingredient, Recipe, IngredientInRecipe])

    yield database

    # Close the database connection and drop the tables
    database.drop_tables([Ingredient, Recipe, IngredientInRecipe])
    database.close()


def test_get_all_recipe_ids(test_database):
    recipe_1 = Recipe.create(name='Pancakes', ingredients_desc='Some ingredients', instructions='Some instructions')
    recipe_2 = Recipe.create(name='Pizza', ingredients_desc='Some ingredients', instructions='Some instructions')
    recipe_3 = Recipe.create(name='Salad', ingredients_desc='Some ingredients', instructions='Some instructions')

    expected = [recipe_1.id, recipe_2.id, recipe_3.id]
    actual = get_all_recipe_ids()

    assert expected == actual


def test_get_recipe_ingredients(test_database):
    recipe = Recipe.create(name='Pancakes', ingredients_desc='Some ingredients', instructions='Some instructions')
    ingredient_1 = Ingredient.create(name="flour")
    ingredient_2 = Ingredient.create(name="eggs")
    IngredientInRecipe.create(ingredient=ingredient_1, recipe=recipe)
    IngredientInRecipe.create(ingredient=ingredient_2, recipe=recipe)

    expected = get_recipe_ingredients(recipe.id)
    actual = [ingredient_1.id, ingredient_2.id]

    assert expected == actual


def test_get_recipes_by_ingredients(test_database):
    recipe_1 = Recipe.create(name='Pancakes', ingredients_desc='Some ingredients', instructions='Some instructions')
    recipe_2 = Recipe.create(name='Pizza', ingredients_desc='Some ingredients', instructions='Some instructions')
    ingredient_1 = Ingredient.create(name="flour")
    ingredient_2 = Ingredient.create(name="eggs")
    IngredientInRecipe.create(ingredient=ingredient_1, recipe=recipe_1)
    IngredientInRecipe.create(ingredient=ingredient_2, recipe=recipe_1)
    IngredientInRecipe.create(ingredient=ingredient_1, recipe=recipe_2)
    IngredientInRecipe.create(ingredient=ingredient_2, recipe=recipe_2)

    expected = ['Pancakes', 'Pizza']
    actual = get_recipes_by_ingredients(['flour', 'eggs'])

    assert expected == actual


def test_get_ids_by_names(test_database):
    ingredient_1 = Ingredient.create(name="flour")
    ingredient_2 = Ingredient.create(name="eggs")

    expected = [ingredient_2.id, ingredient_1.id]
    actual = get_ids_by_names([ingredient_2.name, ingredient_1.name])
    assert expected == actual


def test_get_names_by_ids(test_database):
    recipe_1 = Recipe.create(name='Pancakes', ingredients_desc='Some ingredients', instructions='Some instructions')
    recipe_2 = Recipe.create(name='Pizza', ingredients_desc='Some ingredients', instructions='Some instructions')

    expected = [recipe_1.name, recipe_2.name]
    actual = get_names_by_ids([recipe_1.id, recipe_2.id])
    assert expected == actual


def test_get_details_by_name(test_database):
    recipe = Recipe.create(name='Pancakes', ingredients_desc='Some ingredients', instructions='Some instructions')

    expected = get_details_by_name(recipe.name)
    actual = (recipe.ingredients_desc, recipe.instructions)
    assert expected == actual
