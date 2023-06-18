from peewee import *

database = SqliteDatabase('../database_handler/recipes.db')


# definitions of table models
class Ingredient(Model):
    name = CharField(unique=True)

    class Meta:
        database = database


class Recipe(Model):
    name = CharField(unique=True)
    ingredients_desc = TextField()
    instructions = TextField()

    class Meta:
        database = database


class IngredientInRecipe(Model):
    ingredient = ForeignKeyField(Ingredient)
    recipe = ForeignKeyField(Recipe)

    class Meta:
        database = database


def create_tables():
    with database:
        database.create_tables([Ingredient, Recipe, IngredientInRecipe])


if __name__ == '__main__':
    create_tables()
