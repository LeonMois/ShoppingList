class Ingredient:

    def __init__(self, name: str, type: str) -> None:
        self.name = name
        self.type = type
    
class RecipePart:

    def __init__(self, ingredient: Ingredient, unit: str, amount: float) -> None:
        self.ingredient = ingredient
        self.unit = unit
        self.amount = amount

class Recipe:

    def __init__(self, recipeParts: list) -> None:
        for recipe in recipeParts:
            self.recieParts.append(recipe)
    
    def changeIngredient(self,ingredient, unit, amount) -> None:
        for part in self.recipeParts:
            if part.ingredient.name == ingredient.name:
                part.unit = unit
                part.amount = amount
                return 

