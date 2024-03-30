from sqlite3 import Connection
import sqlite3
from classes import Ingredient, Recipe, RecipePart, SingleItem

def createDBForUser(username: str) -> None:
    con = sqlite3.connect(f"dbs/{username}.db")
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS recipes (id INTEGER PRIMARY KEY,name TEXT UNIQUE);')
    cur.execute('CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY, category TEXT UNIQUE);')
    cur.execute('CREATE TABLE IF NOT EXISTS ingredients (id INTEGER PRIMARY KEY,name TEXT UNIQUE, category TEXT, FOREIGN KEY(category) REFERENCES categories(category));')
    cur.execute('CREATE TABLE IF NOT EXISTS recipeparts (id INTEGER PRIMARY KEY, ingredient TEXT, unit TEXT, amount REAL, recipe_name TEXT, FOREIGN KEY(recipe_name) REFERENCES recipes(name), FOREIGN KEY(ingredient) REFERENCES ingredients(name));')
    cur.execute('CREATE TABLE IF NOT EXISTS singleitems (id INTEGER PRIMARY KEY, name TEXT UNIQUE, unit TEXT, amount REAL, type TEXT);')
    cur.execute('CREATE TABLE IF NOT EXISTS shoppinglist (id INTEGER PRIMARY KEY, name TEXT, unit TEXT, amount REAL, type TEXT, recipe TEXT);')
    cur.execute('CREATE TABLE IF NOT EXISTS settings (id INTEGER PRIMARY KEY, sort_order TEXT, user TEXT UNIQUE);')
    cur.execute("INSERT OR IGNORE INTO settings VALUES (:id, :sort_order, :user)", {"id": 1, "sort_order": " ", "user": username})
    cur.close()
    con.commit()


def setSortOrder(con: Connection, sort_order: str) -> None:
    cur = con.cursor()
    cur.execute("UPDATE settings SET sort_order=:sort_order WHERE id='1'",{"sort_order": sort_order})
    con.commit()
    cur.close()

def getSortOrder(con: Connection):
    cur = con.cursor()
    cur.execute("SELECT (sort_order) FROM settings WHERE id='1';")
    order = cur.fetchone()
    con.commit()
    cur.close()
    return order

def createNewRecipeName(con: Connection, recipe : str) -> None:
    cur = con.cursor()
    cur.execute("INSERT OR IGNORE INTO recipes (name) VALUES (:recipe);", {"recipe": recipe})
    con.commit()
    cur.close()

def createNewCategory(con: Connection, category: str) -> None:
    cur = con.cursor()
    cur.execute("INSERT OR IGNORE INTO categories (category) VALUES (:category)", {"category": category})
    con.commit()
    cur.close()

def createNewIngredient(con: Connection, ingredient: Ingredient) -> None:
    cur = con.cursor()
    cur.execute("INSERT OR IGNORE INTO ingredients name, category VALUES :name, :category", {"name": ingredient.name, "category": ingredient.type})
    con.commit()
    cur.close()

def createNewSingleItem(con: Connection, singleItem: SingleItem) -> None:
    cur = con.cursor()
    cur.execute("INSERT OR IGNORE INTO singleitems (name, unit, amount, type) VALUES (:name, :unit, :amount, :type)", {"name": singleItem.name, "unit": singleItem.unit, "amount": singleItem.amount, "type": singleItem.type})
    con.commit()
    cur.close()

def createNewRecipe(con: Connection, recipe: Recipe) -> None:
    cur = con.cursor()
    for part in recipe.recipeParts:
        cur.execute("INSERT OR IGNORE INTO recipeparts (ingredient, unit, amount,recipe_name) VALUES (:ingredient, :unit, :amount, :recipe_name)", {"ingredient": part.ingredient.name, "unit": part.unit, "amount": part.amount, "recipe_name": recipe.name})
    con.commit()
    cur.close()

def updateRecipe(con: Connection, recipe: Recipe):
    cur = con.cursor()
    cur.execute("DELETE FROM recipeparts WHERE recipe_name=:recipe_name", {"recipe_name": recipe.name})    
    con.commit()
    for part in recipe.recipeParts:
        cur.execute("INSERT OR IGNORE INTO recipeparts (ingredient, unit, amount,recipe_name) VALUES (:ingredient, :unit, :amount, :recipe_name)", {"ingredient": part.ingredient.name, "unit": part.unit, "amount": part.amount, "recipe_name": recipe.name})
    con.commit()
    cur.close()

def addSingleItemToShoppingList(con: Connection, singleItem: SingleItem):
    cur = con.cursor()
    cur.execute("INSERT OR IGNORE INTO shoppinglist (name, unit, amount, type) VALUES (:name, :unit, :amount, :type)", {"name": singleItem.name, "unit": singleItem.unit, "amount": singleItem.amount, "type": singleItem.type})
    con.commit()
    cur.close()

def addRecipeToShoppingList(con: Connection, recipe: Recipe):
    cur = con.cursor()
    for part in recipe.recipeParts:
        cur.execute("INSERT OR IGNORE INTO shoppinglist (name, unit, amount, type, recipe) VALUES (:name, :unit, :amount, :type, :recipe)", {"name": part.ingredient.name, "unit": part.unit, "amount": part.amount, "type": part.ingredient.type, "recipe": recipe.name})
    con.commit()
    cur.close()

def updateSingleItem(con: Connection, singleItem: SingleItem):
    cur = con.cursor()
    cur.execute("DELETE FROM singleitems WHERE name=:item_name", {"item_name": singleItem.name})
    cur.execute("INSERT OR IGNORE INTO singleitems (name, unit, amount, type) VALUES (:name, :unit, :amount, :type)", {"name": singleItem.name, "unit": singleItem.unit, "amount": singleItem.amount, "type": singleItem.type})
    con.commit()
    cur.close()

def renameRecipe(con: Connection, oldName: str, newName: str):
    cur = con.cursor()
    cur.execute("UPDATE recipes SET name=:new_name WHERE name=:old_name", {"new_name": newName, "old_name": oldName})
    cur.execute("UPDATE recipeparts SET recipe_name=:new_name WHERE recipe_name=:old_name", {"new_name": newName, "old_name": oldName})
    con.commit()
    cur.close()

def updateIngredient(con: Connection, ingredient: Ingredient):
    cur = con.cursor()
    cur.execute("Delete FROM ingredients WHERE name=:name", {"name": ingredient.name})
    cur.execute("INSERT OR IGNORE INTO ingredients (name, category) VALUES (:name, :category)", {"name": ingredient.name, "category": ingredient.type})
    con.commit()
    cur.close()

def deleteRecipe(con: Connection, recipe: str):
    cur = con.cursor()
    cur.execute("DELETE FROM recipes WHERE name=:recipe", {"recipe": recipe})
    cur.execute("DELETE FROM recipeparts WHERE recipe_name=:recipe", {"recipe": recipe})
    con.commit()
    cur.close()

def deleteAllShoppingListEntries(con: Connection):
    cur = con.cursor()
    cur.execute("DELETE FROM shoppinglist")
    con.commit()
    cur.close()


def deleteOneItemFromShoppingList(con: Connection, id: int):
    cur = con.cursor()
    cur.execute("DELETE FROM shoppinglist WHERE id=:id", {"id": id})
    con.commit()
    cur.close()

def deleteRecipeFromShoppingList(con: Connection, recipe: str):
    cur = con.cursor()
    cur.execute("DELETE FROM shoppinglist WHERE name=:recipe", {"recipe": recipe})
    con.commit()
    cur.close()

def deleteIngredient(con: Connection, ingredient: str):
    cur = con.cursor()
    cur.execute("DELETE FROM ingredients WHERE name=:ingredient", {"ingredient": ingredient})
    cur.execute("DELETE FROM recipeparts WHERE ingredient=:ingredient", {"ingredient": ingredient})
    con.commit()
    cur.close()

def deleteCategory(con: Connection, category: str):
    cur = con.cursor()
    cur.execute("DELETE FROM categories WHERE category=:category", {"category": category})
    cur.execute("DELETE FROM ingredients WHERE category=:category", {"category": category})
    con.commit()
    cur.close()

def deleteSingleItem(con: Connection, singleItem: str):
    cur = con.cursor()
    cur.execute("DELETE FROM singleitems WHERE name=:singleItem", {"singleItem": singleItem})
    con.commit()
    cur.close()

def getAllRecipes(con: Connection) -> list:
    cur = con.cursor()
    cur.execute("SELECT (name) FROM recipes")
    recipes = cur.fetchall()
    con.commit()
    cur.close()
    return recipes

def getAllIngredients(con: Connection) -> list:
    cur = con.cursor()
    cur.execute("SELECT * FROM ingredients")
    ingredients = cur.fetchall()
    con.commit()
    cur.close()
    return ingredients

def getAllCategories(con: Connection) -> list:
    cur = con.cursor()
    cur.execute("SELECT (category) FROM categories")
    ingredients = cur.fetchall()
    con.commit()
    cur.close()
    return ingredients

def getRecipeByName(con: Connection, recipe: str) -> list:
    cur = con.cursor()
    cur.execute("SELECT * FROM recipeparts WHERE recipe_name=:recipe", {"recipe": recipe})
    fetch = cur.fetchall()
    cur.close()
    return fetch

def getIngredientByName(con: Connection, ingredient: str) -> list:
    cur = con.cursor()
    cur.execute("SELECT * FROM ingredients WHERE name=:ingredient", {"ingredient": ingredient})
    fetch = cur.fetchall()
    cur.close()
    return fetch

def getSingleItems(con: Connection) -> list:
    cur = con.cursor()
    cur.execute("SELECT * FROM singleitems")
    fetch = cur.fetchall()
    cur.close()
    return fetch

def getSingleItemByName(con: Connection, item_name: str) -> list:
    cur = con.cursor()
    cur.execute("SELECT * FROM singleitems WHERE name=:name", {"name": item_name})
    fetch = cur.fetchall()
    cur.close()
    return fetch

def getShoppingListEntries(con: Connection) -> list:
    cur = con.cursor()
    cur.execute("SELECT * FROM shoppinglist")
    fetch = cur.fetchall()
    cur.close()
    return fetch

def getShoppingListEntriesOrdered(con: Connection, order: str) -> list:
    cur = con.cursor()
    cur.execute("SELECT * FROM shoppinglist ORDER BY CASE WHEN type=:order THEN 0 END", {"order": order})
    fetch = cur.fetchall()
    cur.close()
    return fetch
