import sqlite3
import sys


def create_structure(database_name):
    conn = sqlite3.connect(f"{database_name}.sqlite3")

    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS
        Ingredients([ingredient_id] INTEGER PRIMARY KEY AUTOINCREMENT ,
         [ingredient_name] TEXT UNIQUE) ''')

    c.execute('''CREATE TABLE IF NOT EXISTS 
    Recipes([recipe_id] INTEGER PRIMARY KEY NOT NULL,
    [recipe_title] TEXT,
    [specific_ingredients] TEXT,
    [directions] TEXT,
    [ingredients_list] TEX[])''')

    conn.commit()


if __name__ == '__main__':

# python create_database.py database_name
    if len(sys.argv) < 2:
        print("Give the name of the database")
    else:
        create_structure(sys.argv[1])
