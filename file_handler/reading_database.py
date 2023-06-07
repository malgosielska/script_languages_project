import sqlite3


def load_ingredients():
    conn = sqlite3.connect(
        "C:\\Users\\piese\\PycharmProjects\\script_languages_project\\file_handler\\database.sqlite3")
    cursor = conn.cursor()

    cursor.execute('SELECT ingredient_name FROM Ingredients')
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    ingredient_names = [result[0] for result in results]
    return ingredient_names


def load_recipes():
    conn = sqlite3.connect(
        "C:\\Users\\piese\\PycharmProjects\\script_languages_project\\file_handler\\database.sqlite3")
    cursor = conn.cursor()

    cursor.execute('SELECT recipe_id, recipe_title, specific_ingredients, directions FROM Recipes')
    results = cursor.fetchall()

    recipes = []

    # Przetwarzanie wyników zapytania
    for result in results:
        recipe_id = result[0]
        recipe_title = result[1]
        specific_ingredients = result[2]
        directions = result[3]

        # Rozbijanie specific_ingredients na listę składników
        ingredients_list = specific_ingredients.split(',')

        # Tworzenie słownika przepisu
        recipe = {
            'recipe_id': recipe_id,
            'recipe_title': recipe_title,
            'specific_ingredients': specific_ingredients,
            'directions': directions,
            'ingredients_list': ingredients_list
        }

        # Dodawanie słownika przepisu do listy
        recipes.append(recipe)
    cursor.close()
    conn.close()

    return recipes


class database():
    def __init__(self):
        self.ingredients = load_ingredients()
        self.recipes = load_recipes()
