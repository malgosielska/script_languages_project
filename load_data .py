import ast
import csv
import sys
import sqlite3


def load_ingredients(file_name, database_name):
    conn = sqlite3.connect(f'{database_name}.sqlite3')
    c = conn.cursor()
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            file_reader = csv.reader(file)
            next(file_reader)
            for line in file_reader:

                ingredients_list = ast.literal_eval(line[6])
                for ingredient_name in ingredients_list:
                    # Wstawianie składnika do tabeli Ingredients tylko jeśli nazwa nie istnieje już w bazie
                    c.execute("INSERT OR IGNORE INTO Ingredients (ingredient_name) VALUES (?)", (ingredient_name,))

        conn.commit()
    except Exception:
        raise Exception("File not found")


def load_recipes(file_name, database_name):
    conn = sqlite3.connect(f'{database_name}.sqlite3')
    c = conn.cursor()
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            file_reader = csv.reader(file)
            next(file_reader)
            # todo polaczyc jakos liste skladnikow ze skladnikami !
            for line in file_reader:
                recipe_id = line[0]
                recipe_title = line[1]
                recipe_details = format_details(line[2])
                recipe_description = format_description(line[3])
                recipe_ingredients = line[6]

                values = (recipe_id, recipe_title, recipe_details, recipe_description, recipe_ingredients)

                insert_command = 'INSERT INTO Recipes (recipe_id, recipe_title,' \
                                 ' specific_ingredients, directions, ingredients_list) ' \
                                 'VALUES (?, ?, ?, ?, ?)'
                c.execute(insert_command, values)

        conn.commit()
    except Exception:
        raise Exception("File not found")


def format_description(desc):
    desc = ast.literal_eval(desc)
    result = ""
    for i, element in enumerate(desc, start=1):
        result += f"{i}. {element}\n"
    return result


def format_details(details):
    details = ast.literal_eval(details)
    result = "\n".join(details) + "\n"
    return result


def load_file(file_name, database_name):
    load_ingredients(file_name, database_name)
    load_recipes(file_name, database_name)


if __name__ == '__main__':

# python load_data.py Recipes_dataset.csv database_name
    if len(sys.argv) < 3:
        print('Please, give the name of the file and the database')
    else:
        load_file(sys.argv[1], sys.argv[2])
