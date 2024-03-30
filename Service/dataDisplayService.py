from Service.mappingService import mapToSingleItemList, mapToCategoryList, mapToSingleItemList, mapToIngredientList,mapToRecipeNameList
import Repository.recipeRepository as rr
import flask
import sqlite3
userdata = "Leon"
def showDefaultPage(request: flask.request) -> str:
    connection = sqlite3.connect(f"dbs/{userdata}.db")
    order = rr.getSortOrder(connection)[0]
    query = rr.getShoppingListEntriesOrdered(connection,order)
    single_items = mapToSingleItemList(rr.getSingleItems(connection))
    categories = mapToCategoryList(rr.getAllCategories(connection))
    shoppingList = mapToSingleItemList(query)
    connection.close()
    return flask.render_template("index.html", items=shoppingList, single_items=single_items, categories=categories)

def showRecipeEditPage(request: flask.request) -> str:
    connection = sqlite3.connect(f"dbs/{userdata}.db")
    categories = []
    for category in rr.getAllCategories(connection):
        categories.append(category[0])
    ingredients = mapToIngredientList(rr.getAllIngredients(connection))
    recipes = mapToRecipeNameList(rr.getAllRecipes(connection))
    connection.close()
    return flask.render_template("crud_objects.html", categories=categories, ingredients=ingredients, recipes=recipes)

def showListEditPage(request: flask.request) -> str:
    connection = sqlite3.connect(f"dbs/{userdata}.db")
    query = rr.getShoppingListEntries(connection)
    recipes = mapToRecipeNameList(rr.getAllRecipes(connection))
    shoppingList = mapToSingleItemList(query)
    connection.close()
    return flask.render_template("shopping_creation.html", items=shoppingList, recipes=recipes)