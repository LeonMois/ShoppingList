import sqlite3
from sqlite3 import Connection
import classes 

def createDBForUser(username: str) -> None:
    con = sqlite3.connect(f"dbs/{username}.db")
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS recipes (id INTEGER PRIMARY KEY,name TEXT UNIQUE);')
    cur.execute('CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY, category TEXT UNIQUE);')
    cur.execute('CREATE TABLE IF NOT EXISTS ingredients (id INTEGER PRIMARY KEY,name TEXT UNIQUE, category TEXT, FOREIGN KEY(category) REFERENCES categories(category));')
    cur.execute('CREATE TABLE IF NOT EXISTS recipeparts (id INTEGER PRIMARY KEY, recipe_id INTEGER, ingredient TEXT, unit TEXT, amount REAL, recipe_name TEXT, FOREIGN KEY(recipe_name) REFERENCES recipes(name), FOREIGN KEY(ingredient) REFERENCES ingredients(name));')
    cur.close()
    con.commit()

def createRecipe(con: Connection, recipe : str) -> None:
    cur = con.cursor()
    cur.execute(f"INSERT INTO recipes (name) VALUES ('{recipe}');")
    con.commit()
    cur.close()

def createCategory(con: Connection, category: str) -> None:
    cur = con.cursor()
    cur.execute(f"INSERT INTO categories (category) VALUES ('{category}');")
    con.commit()
    cur.close()

def createIngredient(con: Connection, ingredient: classes.Ingredient) -> None:
    cur = con.cursor()
    cur.execute(f"INSERT INTO ingredients (name, category) VALUES ('{ingredient.name}','{ingredient.type}');")
    con.commit()
    cur.close()

def fillRecipe(con: Connection, recipePart: classes.RecipePart, recipe: str) -> None:
    cur = con.cursor()
    cur.execute(f"INSERT INTO recipeparts (ingredient, unit, amount,recipe_name) VALUES ('{recipePart.ingredient.name}','{recipePart.unit}','{recipePart.amount}','{recipe}');")
    con.commit()
    cur.close()

def listRecipes(con: Connection) -> list:
    cur = con.cursor()
    cur.execute(f"SELECT (name) FROM recipes")
    recipes = cur.fetchall()
    con.commit()
    cur.close()
    return recipes

def listIngredients(con: Connection) -> list:
    cur = con.cursor()
    cur.execute(f"SELECT (name) FROM ingredients")
    ingredients = cur.fetchall()
    con.commit()
    cur.close()
    return ingredients

def listCategories(con: Connection) -> list:
    cur = con.cursor()
    cur.execute(f"SELECT (category) FROM categories")
    ingredients = cur.fetchall()
    con.commit()
    cur.close()
    return ingredients

def getRecipe(con: Connection, recipe: str) -> list:
    cur = con.cursor()
    cur.execute(f"SELECT * FROM recipeparts WHERE 'recipe_name'={recipe}")
    fetch = cur.fetchall
    cur.close()
    return fetch


ing = classes.Ingredient(name="Banana",type="fruit")
recipePart = classes.RecipePart(ing,"pieces", "2")
recipe = classes.Recipe([recipePart], "Pizza")

createDBForUser("Leon")
con = sqlite3.connect("dbs/Leon.db")
createRecipe(con,"Pizza")
createCategory(con, "fruit")
createIngredient(con,ing)
fillRecipe(con, recipePart,"Pizza")
print(getRecipe(con,"Pizza"))
print(listCategories(con))
print(listIngredients(con))
print(listRecipes(con))
con.close