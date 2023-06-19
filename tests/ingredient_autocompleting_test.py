import pytest
from peewee import SqliteDatabase
from database_handler.create_database import Ingredient, Recipe, IngredientInRecipe
from database_handler.ingredient_autocompleting import search_ingredients_by_prefix


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


def test_search_ingredients_by_prefix_check_length(test_database):
    prefix = 'chee'
    expected = "cheese"
    test_ingredient = Ingredient.create(name=expected)

    actual_result = search_ingredients_by_prefix(prefix)

    assert len(actual_result) == 1


def test_search_ingredients_by_prefix_check_word(test_database):
    prefix = 'chee'
    expected = "cheese"
    test_ingredient = Ingredient.create(name=expected)

    actual_result = search_ingredients_by_prefix(prefix)

    assert expected in actual_result
