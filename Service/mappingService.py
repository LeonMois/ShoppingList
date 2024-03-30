from classes import Ingredient, Recipe, RecipePart, SingleItem

def mapToIngredientList(rows) -> list[Ingredient]:
    ingredients = []
    for row in rows:
        ingredient =  Ingredient(row[1], row[2])
        ingredients.append(ingredient)
    return ingredients
def mapIngredientsToDict(rows) -> list:
    ingredients = {}
    for row in rows:
        ingredients[row[1]] = row[2]
    return ingredients

def mapsToRecipePartList(rows, ingredients) -> list:
    ingredient_categories = mapIngredientsToDict(ingredients)
    recipeParts = []
    for row in rows:
        ingredient =  Ingredient(row[1], ingredient_categories[row[1]])
        recipePart =  RecipePart(ingredient, row[2], row[3])
        recipeParts.append(recipePart)
    return recipeParts

def mapToSingleItemList(rows) -> list:
    singleItems = []
    for row in rows:
        singleItem =  SingleItem(row[0], row[1], row[2], row[3], row[4])
        singleItems.append(singleItem)
    return singleItems

def mapToCategoryList(rows) -> list:
    categories = []
    for row in rows:
        categories.append(row[0])
    return categories

def mapToRecipeNameList(rows) -> list:
    recipes = []
    for row in rows:
        recipes.append(row[0])
    return recipes

def mapToIngredientList(rows) -> list[Ingredient]:
    ingredients = []
    for row in rows:
        ingredients.append(Ingredient(row[1],row[2]))
    return ingredients

def mapToSingleItem(rows) -> SingleItem:
    row = rows[0]
    return SingleItem(row[0],row[1],row[2],row[3],row[4])
