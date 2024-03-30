class Ingredient:

    def __init__(self, name: str, type: str) -> None:
        self.name = name
        self.type = type

    def __str__(self) -> str:
        return f"{self.name},{self.type}"
    
class RecipePart:

    def __init__(self, ingredient: Ingredient, unit: str, amount: float) -> None:
        self.ingredient = ingredient
        self.unit = unit
        self.amount = amount
    def __str__(self) -> str:
        return f"{self.ingredient.name}, {self.unit}, {self.amount} \n"

class Recipe:

    def __init__(self, recipeParts: list[RecipePart], name: str) -> None:
        self.recipeParts = recipeParts
        self.name = name
    
    def changeIngredient(self,ingredient, unit, amount) -> None:
        for part in self.recipeParts:
            if part.ingredient.name == ingredient.name:
                part.unit = unit
                part.amount = amount
                return 
    
    def __str__(self) -> str:
        printed = f"{self.name}\n"
        for part in self.recipeParts:
            printed += part.__str__()
        return printed
        

class SingleItem:

    def __init__(self, id: int, name: str, unit: str, amount: float, type: str) -> None:
        self.id = id
        self.name = name
        self.unit = unit
        self.amount = amount
        self.type = type
    
    def __str__(self) -> str:
        return f"{self.name},{self.amount},{self.unit}"
    
userdata = "Leon"
