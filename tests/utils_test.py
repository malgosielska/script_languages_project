import pytest
from peewee import SqliteDatabase
from database_handler.create_database import Ingredient, Recipe, IngredientInRecipe
from database_handler.utils import get_recipes_names, get_ingredients_names


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


def test_get_recipes_names(test_database):
    Recipe.create(name='Pancakes', ingredients_desc='Some ingredients', instructions='Some instructions')
    Recipe.create(name='Pizza', ingredients_desc='Some ingredients', instructions='Some instructions')
    Recipe.create(name='Salad', ingredients_desc='Some ingredients', instructions='Some instructions')

    expected = ['Pancakes', 'Pizza', 'Salad']
    actual = get_recipes_names()
    assert actual == expected


def test_get_recipes_names_no_recipes(test_database):
    expected = []
    actual = get_recipes_names()
    assert actual == expected


def test_get_ingredients_names(test_database):
    Ingredient.create(name='Flour')
    Ingredient.create(name='Cheese')
    Ingredient.create(name='Lettuce')

    expected = ['Flour', 'Cheese', 'Lettuce']
    actual = get_ingredients_names()
    assert actual == expected


def test_get_ingredients_names_no_ingredients(test_database):
    expected = []
    actual = get_ingredients_names()
    assert actual == expected
