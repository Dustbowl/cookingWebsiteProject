from models import cost, name, ingredients, direction

class RecipeSubmissionProcess: # this looks more like a function, copied to views.py
    otherClass = RecipeSubmissionForm()
    recipeSubmit = open("DataBase.txt", "a")
    recipeSubmit.write('\n* ')
    recipeSubmit.write(otherClass.name)
    recipeSubmit.write(' & ')
    recipeSubmit.write(otherClass.ingredients)
    recipeSubmit.write(" $ ")
    recipeSubmit.write("10")
    recipeSubmit.write(" : ")
    recipeSubmit.write(otherClass.direction)
    recipeSubmit.close()
    