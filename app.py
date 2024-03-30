import flask
import Repository.recipeRepository as recipeRepository
import Service.dataDisplayService as display
import Service.dataCRUDService as edit_db
import sqlite3
import classes
import Service.mappingService as mappingService
from classes import userdata

    # create and configure the app
def create_app():
    app = flask.Flask(__name__)
    @app.route("/", methods=["GET", "POST"])
    def index():
        if flask.request.method == "GET":
            connection = sqlite3.connect(f"dbs/{userdata}.db")
            recipeRepository.createDBForUser(userdata)
            connection.close() 
            return display.showDefaultPage(flask.request)
        else:
            if "edit" in flask.request.form:
                return flask.redirect("/crud_objects")
            if "shopping" in flask.request.form:
                return flask.redirect("/shoppinglist/creation")

            if "new_item_name" in flask.request.form:
                edit_db.addNewItem(flask.request)
                return flask.redirect("/")
            if "existing_item_name" in flask.request.form:
                edit_db.addExistingItem(flask.request)
                return flask.redirect("/")
            if "sort_order" in flask.request.form:
                edit_db.changeOrdering(flask.request)
                return display.showDefaultPage(flask.request)
            edit_db.deleteItemFromList(flask.request)
            return flask.redirect("/")

    @app.route("/crud_objects", methods=["GET","POST"])
    def recipes():
        if flask.request.method == "GET":
            return display.showRecipeEditPage(flask.request)
        else:
            if "view_list" in flask.request.form:
                return flask.redirect("/")
            elif "edit_shopping" in flask.request.form:
                return flask.redirect("/shoppinglist/creation")
            connection = sqlite3.connect("dbs/Leon.db")
            if flask.request.form.get("add_category") != None:
                edit_db.addNewCategory(flask.request)
            elif flask.request.form.get("delete_category") != None:
                edit_db.deleteCategory(flask.request)
            elif flask.request.form.get("ingredient_name") != None:
                if flask.request.form.get("delete_ingredient") != None:
                    edit_db.deleteIngredient(flask.request)
                    return flask.redirect("/crud_objects")
                edit_db.createOrUpdateIngredient(flask.request)
            elif flask.request.form.get("recipe") == "create_update":
                edit_db.createOrUpdateRecipe(flask.request)     
            elif flask.request.form.get("recipe") == "delete":
                recipeRepository.deleteRecipe(connection,flask.request.form.get("recipe_name"))
            return flask.redirect("/crud_objects")
        
    @app.route("/shoppinglist/creation", methods=["GET","POST"])
    def create_shopping_list():
        if flask.request.method == "GET":
            connection = sqlite3.connect("dbs/Leon.db")
            cur = connection.cursor()    
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            if not "shoppinglist" in cur.fetchall():
                recipeRepository.createDBForUser("Leon")
            cur.close()
            connection.close() 
            return display.showListEditPage(flask.request)
        else:
            if "view_list" in flask.request.form:
                return flask.redirect("/")
            elif "edit_recipes" in flask.request.form:
                return flask.redirect("/crud_objects")
            connection = sqlite3.connect("dbs/Leon.db")
            if flask.request.form.get("recipe") == "add":
                edit_db.addRecipeToShoppingList(flask.request)
            return flask.redirect("/shoppinglist/creation")
    return app