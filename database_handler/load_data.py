import csv
from create_database import Ingredient, Recipe, IngredientInRecipe


def load_data():
    with open('recipes.csv', 'r') as file:
        rows = csv.reader(file, delimiter=',')
        next(rows)

        for row in rows:
            row[2] = row[2].replace('n_l', '\n')
            row[3] = row[3].replace('n_l', '\n')
            recipe_id, recipe_name, ingredients_desc, recipe_instructions, ingredient_names = row
            ingredient_names = ingredient_names.split(',')

            # saving ingredients to the table "ingredients"
            ingredients = []
            for ingredient_name in ingredient_names:
                ingredient, _ = Ingredient.get_or_create(name=ingredient_name.strip())
                ingredients.append(ingredient)

            # saving recipe to the table "recipe"
            recipe = Recipe.create(name=recipe_name, ingredients_desc=ingredients_desc,
                                   instructions=recipe_instructions)

            # connecting recipes with ingredients in a table "ingredientinrecipe"
            for ingredient in ingredients:
                IngredientInRecipe.create(ingredient=ingredient, recipe=recipe)


if __name__ == '__main__':
    load_data()
