import streamlit as st
import repository as repo
import sqlite3
import classes


con = sqlite3.connect("dbs/Leon.db")    
st.title("Welcome to the Recipe Manager")
st.header("What would you like to do?")
st.write("Please select an option from the menu on the left.")
st.sidebar.title("Menu")
option = st.sidebar.radio("Options", ["Shopping List", "Edit Recipes and Items"])

col1, col2 = st.columns(2)
# hide the columns based on the option selected
if option == "Shopping List":
    col1, col2 = st.columns(2)
    col2.empty()
with col1:
    st.write("Shopping List")
    st.write("Here is your shopping list")
    repo.createDBForUser("Leon")
    connection = sqlite3.connect("dbs/Leon.db")
    shoppingList = repo.getShoppingList(connection)
    # Display the shopping list as checkboxes with the name of the item and the amount and the unit
    for item in shoppingList:
        st.checkbox(f"{item[1]} {item[2]} {item[3]}")
    # Display a button to clear the shopping list
    if st.button("Clear Shopping List"):
        repo.clearShoppingList()

with col2:
    st.write("Create a new recipe")
    recipeName = st.text_input("Recipe Name")
    ingredientName = st.text_input("Ingredients")
    ingredientType = st.text_input("Type")
    unit = st.text_input("Unit")
    recipeAmounts = st.text_input("Amounts")
    # Display a button to add the recipe to the database
    if st.button("Add Recipe"):
        ingredient = classes.Ingredient(ingredientName, ingredientType)
        recipePart = classes.RecipePart(ingredient, unit, recipeAmounts)
        repo.createRecipe(con, recipeName)
        repo.createCategory(con, ingredientType)
        repo.createIngredient(con, ingredient)
        repo.fillRecipe(con, recipePart, recipeName)
    # Dropdown to select a recipe to add to list
    st.write("Add a recipe to the shopping list")
    recipe = st.selectbox("Recipe", repo.listRecipes(con))
    if st.button("Add Recipe to Shopping List"):
        completeRecipe = repo.getRecipe(con, recipe)
        recipeParts = []
        for part in completeRecipe:
            ingredient = classes.Ingredient(part[1], part[2])
            recipePart = classes.RecipePart(ingredient, part[3], part[4])
            recipeParts.append(recipePart)
            
        recipe = classes.Recipe(recipeParts, recipe)

        repo.addRecipeToShoppingList(con, recipe)
