import flask
import repository
import sqlite3
import classes
import mappings

app = flask.Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if flask.request.method == "GET":
        connection = sqlite3.connect("dbs/Leon.db")
        query = repository.getShoppingList(connection)
        connection.close() 
        shoppingList = mappings.mapRowsToSingleItems(query)
        return flask.render_template("index.html", items=shoppingList)
    else:
        connection = sqlite3.connect("dbs/Leon.db")
        repository.deleteItemFromShoppingList(connection, flask.request.form.get("action"))
        connection.close()
        return flask.redirect("/")

@app.route("/crud_objects", methods=["GET","POST"])
def recipes():
    if flask.request.method == "GET":
        connection = sqlite3.connect("dbs/Leon.db")
        categories = []
        for category in repository.listCategories(connection):
            categories.append(category[0])
        print(repository.listIngredients(connection))
        ingredients = mappings.mapRowsToIngredients(repository.listIngredients(connection))
        return flask.render_template("crud_objects.html", categories=categories, ingredients=ingredients)
    else:
        connection = sqlite3.connect("dbs/Leon.db")
        if flask.request.form.get("add_category") != None:
            repository.createCategory(connection, flask.request.form.get("add_category"))
        elif flask.request.form.get("delete_category") != None:
            repository.deleteCategory(connection, flask.request.form.get("delete_category"))
        elif flask.request.form.get("ingredient_name") != None:
            if flask.request.form.get("delete_ingredient") != None:
                repository.deleteIngredient(connection, flask.request.form.get("delete_ingredient"))
                return flask.redirect("/crud_objects")
            ingredients = mappings.mapRowsToIngredients(repository.listIngredients(connection))
            print(ingredients)
            userIngredient = classes.Ingredient(flask.request.form.get("ingredient_name"), flask.request.form.get("ingredient_category"))
            for ingredient in ingredients:
                if ingredient.name == userIngredient.name:
                    repository.updateIngredient(connection, userIngredient)
                    return flask.redirect("/crud_objects")
            repository.createIngredient(connection, userIngredient)
        connection.close()
        return flask.redirect("/crud_objects")