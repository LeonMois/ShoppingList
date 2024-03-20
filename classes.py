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

    def __init__(self, recipeParts: list, name: str) -> None:
        self.recipeParts = recipeParts
        self.name = name
    
    def changeIngredient(self,ingredient, unit, amount) -> None:
        for part in self.recipeParts:
            if part.ingredient.name == ingredient.name:
                part.unit = unit
                part.amount = amount
                return 

class SingleItem:

    def __init__(self, id: int, name: str, unit: str, amount: float, type: str) -> None:
        self.id = id
        self.name = name
        self.unit = unit
        self.amount = amount
        self.type = type