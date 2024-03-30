import flask
import recipeRepository
import sqlite3
import classes
import mappingService

    # create and configure the app
def create_app():
    app = flask.Flask(__name__)
    @app.route("/", methods=["GET", "POST"])
    def index():
        if flask.request.method == "GET":
            connection = sqlite3.connect("dbs/Leon.db")
            recipeRepository.createDBForUser("Leon")
            query = recipeRepository.getShoppingList(connection)
            single_items = mappingService.mapRowsToSingleItems(recipeRepository.getSingleItems(connection))
            categories = mappingService.mapRowsToCategories(recipeRepository.listCategories(connection))

            shoppingList = mappingService.mapRowsToSingleItems(query)
            for part in shoppingList:
                if part.type == recipeRepository.getSortOrder(connection)[0][0]:
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
                recipeRepository.addSingleItemToShoppingList(connection,item)
                recipeRepository.createCategory(connection, type)
                item.amount = None
                item.unit = None
                recipeRepository.createSingleItem(connection, item)
                return flask.redirect("/")
            if "existing_item_name" in flask.request.form:
                name = flask.request.form.get("existing_item_name")
                item = mappingService.mapRowToSingleItem(recipeRepository.getOneSingleItem(connection,name))
                item.amount = flask.request.form.get("amount")
                item.unit = flask.request.form.get("unit")
                recipeRepository.addSingleItemToShoppingList(connection,item)
                return flask.redirect("/")
            if "sort_order" in flask.request.form:
                sort_order = flask.request.form.get("sort_order")
                recipeRepository.setSortOrder(connection,sort_order)
                query = recipeRepository.getShoppingList(connection)
                single_items = mappingService.mapRowsToSingleItems(recipeRepository.getSingleItems(connection))
                categories = mappingService.mapRowsToCategories(recipeRepository.listCategories(connection))
                connection.close() 
                shoppingList = mappingService.mapRowsToSingleItems(query)
                for part in shoppingList:
                    if part.type == sort_order:
                        tmp = part
                        shoppingList.remove(part)
                        shoppingList.insert(0,tmp)
                return flask.render_template("index.html", items=shoppingList, single_items=single_items, categories = categories)
            recipeRepository.deleteItemFromShoppingList(connection, flask.request.form.get("action"))
            connection.close()
            return flask.redirect("/")

    @app.route("/crud_objects", methods=["GET","POST"])
    def recipes():
        if flask.request.method == "GET":
            connection = sqlite3.connect("dbs/Leon.db")
            categories = []
            for category in recipeRepository.listCategories(connection):
                categories.append(category[0])
            ingredients = mappingService.mapRowsToIngredients(recipeRepository.listIngredients(connection))
            recipes = mappingService.mapRowsToRecipe(recipeRepository.listRecipes(connection))
            return flask.render_template("crud_objects.html", categories=categories, ingredients=ingredients, recipes=recipes)
        else:
            if "view_list" in flask.request.form:
                return flask.redirect("/")
            elif "edit_shopping" in flask.request.form:
                return flask.redirect("/shoppinglist/creation")
            connection = sqlite3.connect("dbs/Leon.db")
            if flask.request.form.get("add_category") != None:
                recipeRepository.createCategory(connection, flask.request.form.get("add_category"))
            elif flask.request.form.get("delete_category") != None:
                recipeRepository.deleteCategory(connection, flask.request.form.get("delete_category"))
            elif flask.request.form.get("ingredient_name") != None:
                if flask.request.form.get("delete_ingredient") != None:
                    recipeRepository.deleteIngredient(connection, flask.request.form.get("delete_ingredient"))
                    return flask.redirect("/crud_objects")
                ingredients = mappingService.mapRowsToIngredients(recipeRepository.listIngredients(connection))
    
                userIngredient = classes.Ingredient(flask.request.form.get("ingredient_name"), flask.request.form.get("ingredient_category"))
                for ingredient in ingredients:
                    if ingredient.name == userIngredient.name:
                        recipeRepository.updateIngredient(connection, userIngredient)
                        return flask.redirect("/crud_objects")
                recipeRepository.createIngredient(connection, userIngredient)
            elif flask.request.form.get("recipe") == "create_update":
                ingredients = mappingService.mapRowsToIngredientKeyValue(recipeRepository.listIngredients(connection))
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
                if flask.request.form.get("recipe_name") in mappingService.mapRowsToRecipe(recipeRepository.listRecipes(connection)):
                    recipeRepository.updateRecipe(connection, recipe)
                else:
                    recipeRepository.createRecipe(connection, recipe.name)
                    recipeRepository.fillRecipe(connection, recipe)       
            elif flask.request.form.get("recipe") == "delete":
                recipeRepository.deleteRecipe(connection,flask.request.form.get("recipe_name"))
            connection.close()
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
            query = recipeRepository.getShoppingList(connection)
            recipes = mappingService.mapRowsToRecipe(recipeRepository.listRecipes(connection))
            connection.close() 
            shoppingList = mappingService.mapRowsToSingleItems(query)
            return flask.render_template("shopping_creation.html", items=shoppingList, recipes=recipes)
        else:
            if "view_list" in flask.request.form:
                return flask.redirect("/")
            elif "edit_recipes" in flask.request.form:
                return flask.redirect("/crud_objects")
            connection = sqlite3.connect("dbs/Leon.db")
            if flask.request.form.get("recipe") == "add":
                ingredients = recipeRepository.listIngredients(connection)
                recipe = classes.Recipe(mappingService.mapsRowsToRecipeParts(recipeRepository.getRecipe(connection,flask.request.form.get("recipe_name")),ingredients),flask.request.form.get("recipe_name"))
                recipeRepository.addRecipeToShoppingList(connection,recipe)
            return flask.redirect("/shoppinglist/creation")
    return app