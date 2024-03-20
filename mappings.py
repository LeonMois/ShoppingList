import classes

def mapRowsToIngredients(rows) -> list[classes.Ingredient]:
    ingredients = []
    for row in rows:
        ingredient = classes.Ingredient(row[1], row[2])
        ingredients.append(ingredient)
    return ingredients

def mapsRowsToRecipeParts(rows) -> list:
    recipeParts = []
    for row in rows:
        ingredient = classes.Ingredient(row["name"], row["category"])
        recipePart = classes.RecipePart(ingredient, row["unit"], row["amount"])
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