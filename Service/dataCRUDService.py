from Service.mappingService import mapToSingleItem, mapToIngredientList,mapIngredientsToDict,mapToRecipeNameList,mapsToRecipePartList
import Repository.recipeRepository as rr
import sqlite3
import flask
from classes import Ingredient, Recipe, RecipePart, SingleItem
userdata = "Leon"
    
def addNewItem(request: flask.request):
    connection = sqlite3.connect(f"dbs/{userdata}.db")
    item_name = request.form.get("new_item_name")
    unit = request.form.get("unit")
    amount = request.form.get("amount")
    type = request.form.get("type")
    item = SingleItem(0,item_name,unit,amount,type)
    rr.addSingleItemToShoppingList(connection,item)
    rr.createNewCategory(connection, type)
    item.amount = None
    item.unit = None
    rr.createNewSingleItem(connection, item)
    connection.close()

def addExistingItem(request: flask.request):
    connection = sqlite3.connect(f"dbs/{userdata}.db")
    name = request.form.get("existing_item_name")
    item = mapToSingleItem(rr.getSingleItemByName(connection,name))
    item.amount = request.form.get("amount")
    item.unit = request.form.get("unit")
    rr.addSingleItemToShoppingList(connection,item)
    connection.close()

def changeOrdering(request: flask.request):
    sort_order = request.form.get("sort_order")
    connection = sqlite3.connect(f"dbs/{userdata}.db")
    rr.setSortOrder(connection,sort_order)
    connection.close()

def deleteItemFromList(request: flask.request):
    connection = sqlite3.connect("dbs/Leon.db")
    rr.deleteOneItemFromShoppingList(connection, request.form.get("action"))
    connection.close()
    
def addNewCategory(request: flask.request):
    connection = sqlite3.connect("dbs/Leon.db")
    rr.createNewCategory(connection, request.form.get("add_category"))
    connection.close()

def deleteCategory(request: flask.request):
    connection = sqlite3.connect("dbs/Leon.db")
    rr.deleteCategory(connection, request.form.get("delete_category"))
    connection.close()

def deleteIngredient(request: flask.request):
    connection = sqlite3.connect("dbs/Leon.db")
    rr.deleteIngredient(connection, request.form.get("delete_ingredient"))
    connection.close()

def createOrUpdateIngredient(request: flask.request):
    connection = sqlite3.connect("dbs/Leon.db")
    ingredients = mapToIngredientList(rr.getAllIngredients(connection))
    userIngredient = Ingredient(request.form.get("ingredient_name"), request.form.get("ingredient_category"))
    for ingredient in ingredients:
        if ingredient.name == userIngredient.name:
            rr.updateIngredient(connection, userIngredient)
            connection.close()
            return
    rr.createNewIngredient(connection, userIngredient)
    connection.close()

def createOrUpdateRecipe(request: flask.request):
    connection = sqlite3.connect("dbs/Leon.db")
    ingredients = mapIngredientsToDict(rr.getAllIngredients(connection))
    i = 0
    recipe_parts = []
    while(request.form.get("recipe_ingredient_" + str(i)) != None):
        ingredient = request.form.get("recipe_ingredient_" + str(i))
        amount = request.form.get("amount_" + str(i))
        unit = request.form.get("unit_" + str(i))
        ing = Ingredient(ingredient, ingredients[ingredient])
        recipe_parts.append(RecipePart(ing,unit,amount))
        i += 1
    recipe = Recipe(recipe_parts, request.form.get("recipe_name"))
    if request.form.get("recipe_name") in mapToRecipeNameList(rr.getAllRecipes(connection)):
        rr.updateRecipe(connection, recipe)
    else:
        rr.createNewRecipeName(connection, recipe.name)
        rr.createNewRecipe(connection, recipe)  
    connection.close()

def addRecipeToShoppingList(request: flask.request):
    connection = sqlite3.connect("dbs/Leon.db")
    ingredients = rr.getAllIngredients(connection)
    recipe = Recipe(mapsToRecipePartList(rr.getRecipeByName(connection,request.form.get("recipe_name")),ingredients),request.form.get("recipe_name"))
    rr.addRecipeToShoppingList(connection,recipe)
    connection.close()