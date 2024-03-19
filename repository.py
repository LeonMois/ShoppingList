import sqlite3
from sqlite3 import Connection
import classes 

def createDBForUser(username: str) -> None:
    con = sqlite3.connect(f"dbs/{username}.db")
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS recipes (id INTEGER PRIMARY KEY,name TEXT UNIQUE);')
    cur.execute('CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY, category TEXT UNIQUE);')
    cur.execute('CREATE TABLE IF NOT EXISTS ingredients (id INTEGER PRIMARY KEY,name TEXT UNIQUE, category TEXT, FOREIGN KEY(category) REFERENCES categories(category));')
    cur.execute('CREATE TABLE IF NOT EXISTS recipeparts (id INTEGER PRIMARY KEY, ingredient TEXT, unit TEXT, amount REAL, recipe_name TEXT, FOREIGN KEY(recipe_name) REFERENCES recipes(name), FOREIGN KEY(ingredient) REFERENCES ingredients(name));')
    cur.execute('CREATE TABLE IF NOT EXISTS singleitems (id INTEGER PRIMARY KEY, name TEXT UNIQUE, unit TEXT, amount REAL, type TEXT);')
    cur.execute('CREATE TABLE IF NOT EXISTS shoppinglist (id INTEGER PRIMARY KEY, name TEXT, unit TEXT, amount REAL, type TEXT, recipe TEXT);')
    cur.close()
    con.commit()


def createRecipe(con: Connection, recipe : str) -> None:
    cur = con.cursor()
    cur.execute(f"INSERT OR IGNORE INTO recipes (name) VALUES ('{recipe}');")
    con.commit()
    cur.close()

def createCategory(con: Connection, category: str) -> None:
    cur = con.cursor()
    cur.execute(f"INSERT OR IGNORE INTO categories (category) VALUES ('{category}');")
    con.commit()
    cur.close()

def createIngredient(con: Connection, ingredient: classes.Ingredient) -> None:
    cur = con.cursor()
    cur.execute(f"INSERT OR IGNORE INTO ingredients (name, category) VALUES ('{ingredient.name}','{ingredient.type}');")
    con.commit()
    cur.close()

def createSingleItem(con: Connection, singleItem: classes.SingleItem) -> None:
    cur = con.cursor()
    cur.execute(f"INSERT OR IGNORE INTO singleitems (name, unit, amount, type) VALUES ('{singleItem.name}','{singleItem.unit}','{singleItem.amount}','{singleItem.type}');")
    con.commit()
    cur.close()

def fillRecipe(con: Connection, recipePart: classes.RecipePart, recipe: str) -> None:
    cur = con.cursor()
    cur.execute(f"INSERT OR IGNORE INTO recipeparts (ingredient, unit, amount,recipe_name) VALUES ('{recipePart.ingredient.name}','{recipePart.unit}','{recipePart.amount}','{recipe}');")
    con.commit()
    cur.close()

def updateRecipe(con: Connection, recipe: classes.Recipe):
    cur = con.cursor()
    cur.execute(f"DELETE FROM recipeparts WHERE recipe_name='{recipe.name}'")
    for part in recipe.recipeParts:
        cur.execute(f"INSERT OR IGNORE INTO recipeparts (ingredient, unit, amount,recipe_name) VALUES ('{part.ingredient.name}','{part.unit}','{part.amount}','{recipe.name}');")
    con.commit()
    cur.close()

def addSingleItemToShoppingList(con: Connection, singleItem: classes.SingleItem):
    cur = con.cursor()
    cur.execute(f"INSERT OR IGNORE INTO shoppinglist (name, unit, amount, type) VALUES ('{singleItem.name}','{singleItem.unit}','{singleItem.amount}','{singleItem.type}');")
    con.commit()
    cur.close()

def addRecipeToShoppingList(con: Connection, recipe: classes.Recipe):
    cur = con.cursor()
    for part in recipe.recipeParts:
        cur.execute(f"INSERT OR IGNORE INTO shoppinglist (name, unit, amount, type, recipe) VALUES ('{part.ingredient.name}','{part.unit}','{part.amount}','{part.ingredient.type}','{recipe.name}');")
    con.commit()
    cur.close()

def updateSingleItem(con: Connection, singleItem: classes.SingleItem):
    cur = con.cursor()
    cur.execute(f"DELETE FROM singleitems WHERE name='{singleItem.name}'")
    cur.execute(f"INSERT OR IGNORE INTO singleitems (name, unit, amount, type) VALUES ('{singleItem.name}','{singleItem.unit}','{singleItem.amount}','{singleItem.type}');")
    con.commit()
    cur.close()

def renameRecipe(con: Connection, oldName: str, newName: str):
    cur = con.cursor()
    cur.execute(f"UPDATE recipes SET name='{newName}' WHERE name='{oldName}'")
    cur.execute(f"UPDATE recipeparts SET recipe_name='{newName}' WHERE recipe_name='{oldName}'")
    con.commit()
    cur.close()

def updateIngredient(con: Connection, ingredient: classes.Ingredient):
    cur = con.cursor()
    cur.execute(f"DELETE FROM ingredients WHERE name='{ingredient.name}'")
    cur.execute(f"INSERT OR IGNORE INTO ingredients (name, category) VALUES ('{ingredient.name}','{ingredient.type}');")
    con.commit()
    cur.close()

def deleteRecipe(con: Connection, recipe: str):
    cur = con.cursor()
    cur.execute(f"DELETE FROM recipes WHERE name='{recipe}'")
    cur.execute(f"DELETE FROM recipeparts WHERE recipe_name='{recipe}'")
    con.commit()
    cur.close()

def deleteShoppingList(con: Connection):
    cur = con.cursor()
    cur.execute(f"DELETE FROM shoppinglist")
    con.commit()
    cur.close()


def deleteItemFromShoppingList(con: Connection, id: int):
    cur = con.cursor()
    cur.execute(f"DELETE FROM shoppinglist WHERE id='{id}'")
    con.commit()
    cur.close()

def deleteRecipeFromShoppingList(con: Connection, recipe: str):
    cur = con.cursor()
    cur.execute(f"DELETE FROM shoppinglist WHERE name='{recipe}'")
    con.commit()
    cur.close()
def deleteIngredient(con: Connection, ingredient: str):
    cur = con.cursor()
    cur.execute(f"DELETE FROM ingredients WHERE name='{ingredient}'")
    cur.execute(f"DELETE FROM recipeparts WHERE ingredient='{ingredient}'")
    con.commit()
    cur.close()

def deleteCategory(con: Connection, category: str):
    cur = con.cursor()
    cur.execute(f"DELETE FROM categories WHERE category='{category}'")
    cur.execute(f"DELETE FROM ingredients WHERE category='{category}'")
    con.commit()
    cur.close()

def deleteSingleItem(con: Connection, singleItem: str):
    cur = con.cursor()
    cur.execute(f"DELETE FROM singleitems WHERE name='{singleItem}'")
    con.commit()
    cur.close()

def listRecipes(con: Connection) -> list:
    cur = con.cursor()
    cur.execute(f"SELECT (name) FROM recipes")
    recipes = [recipe[0] for recipe in cur.fetchall()]

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
    cur.execute(f"SELECT * FROM recipeparts WHERE recipe_name='{recipe}'")
    fetch = cur.fetchall()
    cur.close()
    return fetch

def getSingleItems(con: Connection) -> list:
    cur = con.cursor()
    cur.execute(f"SELECT * FROM singleitems")
    fetch = cur.fetchall()
    cur.close()
    return fetch
def getShoppingList(con: Connection) -> list:
    cur = con.cursor()
    cur.execute(f"SELECT * FROM shoppinglist")
    fetch = cur.fetchall()
    cur.close()
    return fetch

#ing = classes.Ingredient(name="Banana",type="fruit")
#recipePart = classes.RecipePart(ing,"pieces", "2")
#recipe = classes.Recipe([recipePart], "Pizza")

#createDBForUser("Leon")
#con = sqlite3.connect("dbs/Leon.db")
#createRecipe(con,"Pizza")
#createCategory(con, "fruit")
#createIngredient(con,ing)
#fillRecipe(con, recipePart,"Pizza")
#print(getRecipe(con,"Pizza"))
#print(listCategories(con))
#print(listIngredients(con))
#print(listRecipes(con))
#con.close