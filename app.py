import flask
import repository
import sqlite3
import classes
import mappings

    # create and configure the app
def create_app():
    app = flask.Flask(__name__)
    @app.route("/", methods=["GET", "POST"])
    def index():
        if flask.request.method == "GET":
            connection = sqlite3.connect("dbs/Leon.db")
            repository.createDBForUser("Leon")
            query = repository.getShoppingList(connection)
            single_items = mappings.mapRowsToSingleItems(repository.getSingleItems(connection))
            categories = mappings.mapRowsToCategories(repository.listCategories(connection))

            shoppingList = mappings.mapRowsToSingleItems(query)
            for part in shoppingList:
                if part.type == repository.getSortOrder(connection)[0][0]:
                    tmp = part
                    shoppingList.remove(part)
                    shoppingList.insert(0,tmp)
            connection.close() 
            return flask.render_template("index.html", items=shoppingList, single_items=single_items, categories=categories)
        else:
            if "edit" in flask.request.form:
                return flask.redirect("/crud_objects")
            if "shopping" in flask.request.form:
                return flask.redirect("/shoppinglist/creation")
            connection = sqlite3.connect("dbs/Leon.db")
            if "new_item_name" in flask.request.form:
                name = flask.request.form.get("new_item_name")
                unit = flask.request.form.get("unit")
                amount = flask.request.form.get("amount")
                type = flask.request.form.get("type")
                item = classes.SingleItem(0,name,unit,amount,type)
                repository.addSingleItemToShoppingList(connection,item)
                repository.createCategory(connection, type)
                item.amount = None
                item.unit = None
                repository.createSingleItem(connection, item)
                return flask.redirect("/")
            if "existing_item_name" in flask.request.form:
                name = flask.request.form.get("existing_item_name")
                item = mappings.mapRowToSingleItem(repository.getOneSingleItem(connection,name))
                item.amount = flask.request.form.get("amount")
                item.unit = flask.request.form.get("unit")
                repository.addSingleItemToShoppingList(connection,item)
                return flask.redirect("/")
            if "sort_order" in flask.request.form:
                sort_order = flask.request.form.get("sort_order")
                repository.setSortOrder(connection,sort_order)
                query = repository.getShoppingList(connection)
                single_items = mappings.mapRowsToSingleItems(repository.getSingleItems(connection))
                categories = mappings.mapRowsToCategories(repository.listCategories(connection))
                connection.close() 
                shoppingList = mappings.mapRowsToSingleItems(query)
                for part in shoppingList:
                    if part.type == sort_order:
                        tmp = part
                        shoppingList.remove(part)
                        shoppingList.insert(0,tmp)
                return flask.render_template("index.html", items=shoppingList, single_items=single_items, categories = categories)
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
            ingredients = mappings.mapRowsToIngredients(repository.listIngredients(connection))
            recipes = mappings.mapRowsToRecipe(repository.listRecipes(connection))
            return flask.render_template("crud_objects.html", categories=categories, ingredients=ingredients, recipes=recipes)
        else:
            if "view_list" in flask.request.form:
                return flask.redirect("/")
            elif "edit_shopping" in flask.request.form:
                return flask.redirect("/shoppinglist/creation")
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
    
                userIngredient = classes.Ingredient(flask.request.form.get("ingredient_name"), flask.request.form.get("ingredient_category"))
                for ingredient in ingredients:
                    if ingredient.name == userIngredient.name:
                        repository.updateIngredient(connection, userIngredient)
                        return flask.redirect("/crud_objects")
                repository.createIngredient(connection, userIngredient)
            elif flask.request.form.get("recipe") == "create_update":
                ingredients = mappings.mapRowsToIngredientKeyValue(repository.listIngredients(connection))
                i = 0
                recipe_parts = []
                while(flask.request.form.get("recipe_ingredient_" + str(i)) != None):
                    ingredient = flask.request.form.get("recipe_ingredient_"+str(i))
                    amount = flask.request.form.get("amount_"+str(i))
                    unit = flask.request.form.get("unit_"+str(i))
                    ing = classes.Ingredient(ingredient, ingredients[ingredient])
                    recipe_parts.append(classes.RecipePart(ing,unit,amount))
                    i += 1
                recipe = classes.Recipe(recipe_parts, flask.request.form.get("recipe_name"))
                if flask.request.form.get("recipe_name") in mappings.mapRowsToRecipe(repository.listRecipes(connection)):
                    repository.updateRecipe(connection, recipe)
                else:
                    repository.createRecipe(connection, recipe.name)
                    repository.fillRecipe(connection, recipe)       
            elif flask.request.form.get("recipe") == "delete":
                repository.deleteRecipe(connection,flask.request.form.get("recipe_name"))
            connection.close()
            return flask.redirect("/crud_objects")
        
    @app.route("/shoppinglist/creation", methods=["GET","POST"])
    def create_shopping_list():
        if flask.request.method == "GET":
            connection = sqlite3.connect("dbs/Leon.db")
            cur = connection.cursor()    
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            if not "shoppinglist" in cur.fetchall():
                repository.createDBForUser("Leon")
            cur.close()
            query = repository.getShoppingList(connection)
            recipes = mappings.mapRowsToRecipe(repository.listRecipes(connection))
            connection.close() 
            shoppingList = mappings.mapRowsToSingleItems(query)
            return flask.render_template("shopping_creation.html", items=shoppingList, recipes=recipes)
        else:
            if "view_list" in flask.request.form:
                return flask.redirect("/")
            elif "edit_recipes" in flask.request.form:
                return flask.redirect("/crud_objects")
            connection = sqlite3.connect("dbs/Leon.db")
            if flask.request.form.get("recipe") == "add":
                ingredients = repository.listIngredients(connection)
                recipe = classes.Recipe(mappings.mapsRowsToRecipeParts(repository.getRecipe(connection,flask.request.form.get("recipe_name")),ingredients),flask.request.form.get("recipe_name"))
                repository.addRecipeToShoppingList(connection,recipe)
            return flask.redirect("/shoppinglist/creation")
    return app