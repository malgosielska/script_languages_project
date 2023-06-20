import pytest
from peewee import SqliteDatabase

from database_handler.create_database import Ingredient, Recipe, IngredientInRecipe


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


def test_ingredient_table_exists(test_database):
    # Check if the Ingredient table is created correctly
    assert Ingredient.table_exists()


def test_recipe_table_exists(test_database):
    # Check if the Recipe table is created correctly
    assert Recipe.table_exists()


def test_ingredient_in_recipe_table_exists(test_database):
    # Check if the IngredientInRecipe table is created correctly
    assert IngredientInRecipe.table_exists()


def test_ingredient_unique_name(test_database):
    # Check if the 'name' field in Ingredient is unique
    ingredient1 = Ingredient.create(name='Salt')
    with pytest.raises(Exception):
        Ingredient.create(name='Salt')  # Should raise an exception


def test_recipe_unique_name(test_database):
    # Check if the 'name' field in Recipe is unique
    recipe1 = Recipe.create(name='Pasta', ingredients_desc='Some ingredients', instructions='Some instructions')
    with pytest.raises(Exception):
        Recipe.create(name='Pasta', ingredients_desc='Some ingredients', instructions='Some instructions')


def test_ingredient_in_recipe_ingredient(test_database):
    # Check if the IngredientInRecipe relationship has the correct ingredient
    ingredient1 = Ingredient.create(name='Salt')
    recipe1 = Recipe.create(name='Pasta', ingredients_desc='Some ingredients', instructions='Some instructions')
    ingredient_in_recipe = IngredientInRecipe.create(ingredient=ingredient1, recipe=recipe1)

    assert ingredient_in_recipe.ingredient == ingredient1


def test_ingredient_in_recipe_recipe(test_database):
    # Check if the IngredientInRecipe relationship has the correct recipe
    ingredient1 = Ingredient.create(name='Salt')
    recipe1 = Recipe.create(name='Pasta', ingredients_desc='Some ingredients', instructions='Some instructions')
    ingredient_in_recipe = IngredientInRecipe.create(ingredient=ingredient1, recipe=recipe1)

    assert ingredient_in_recipe.recipe == recipe1
