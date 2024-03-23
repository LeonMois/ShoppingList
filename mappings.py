import classes

def mapRowsToIngredients(rows) -> list[classes.Ingredient]:
    ingredients = []
    for row in rows:
        ingredient = classes.Ingredient(row[1], row[2])
        ingredients.append(ingredient)
    return ingredients
def mapRowsToIngredientKeyValue(rows) -> list:
    ingredients = {}
    for row in rows:
        ingredients[row[1]] = row[2]
    return ingredients

def mapsRowsToRecipeParts(rows, ingredients) -> list:
    ingredient_categories = mapRowsToIngredientKeyValue(ingredients)
    recipeParts = []
    for row in rows:
        ingredient = classes.Ingredient(row[1], ingredient_categories[row[1]])
        recipePart = classes.RecipePart(ingredient, row[2], row[3])
        recipeParts.append(recipePart)
    return recipeParts

def mapRowsToSingleItems(rows) -> list:
    singleItems = []
    for row in rows:
        singleItem = classes.SingleItem(row[0], row[1], row[2], row[3], row[4])
        singleItems.append(singleItem)
    return singleItems

def mapRowsToCategories(rows) -> list:
    categories = []
    for row in rows:
        categories.append(row[1])
    return categories

def mapRowsToRecipe(rows) -> list:
    recipes = []
    for row in rows:
        recipes.append(row[0])
    return recipes

def mapRowsToIngredients(rows) -> classes.Ingredient:
    ingredients = []
    for row in rows:
        ingredients.append(classes.Ingredient(row[1],row[2]))
    return ingredients