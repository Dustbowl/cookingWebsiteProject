from django.db import models
from django import forms
from .Filter import Filter
from .PriceFilter import PriceFilter
from .NameFilter import NameFilter
from .IngredientFilter import IngredientFilter

price_range = (
    ('under_5','Under $5'),
    ('5_10','$5-$10'),
    ('10-15','$10-$15'),
)

days = (
    ('Sunday','Sunday'),
    ('Monday','Monday'),
    ('Tuesday','Tuesday'),
    ('Wednesday','Wednesday'),
    ('Thursday','Thursday'),
    ('Friday','Friday'),
    ('Saturday','Saturday'),
)
meals = (
    ('Breakfast','Breakfast'),
    ('Lunch','Lunch'),
    ('Dinner','Dinner'),
)
        
class MealPlanForm (forms.Form):
    name = forms.CharField(label="Meal Name")
    day = forms.CharField(label='Day', widget=forms.Select(choices= days))
    meal = forms.CharField(label='Meal', widget=forms.Select(choices= meals))

class SearchToolForm (forms.Form):
    price_filter = forms.CharField(widget=forms.Select(choices=price_range), required=False)
    name = forms.CharField(label="Name", required=False)
    ingredients = forms.CharField(label="Ingredients",widget=forms.Textarea(), required=False)

class RecipeSubmissionForm (forms.Form):
    #cost = forms.CharField(widget=forms.Select(choices=price_range))
    cost = forms.CharField(label="Cost")
    name = forms.CharField(label="Name")
    ingredients = forms.CharField(label="Ingredients",widget=forms.Textarea())
    direction = forms.CharField(label="Direction",widget=forms.Textarea())

#developed by Jacob Dickson
#adds the meal to the correct spot in the MealPlanTemplate.txt
#name = string, name of meal
#day = string, day of the week
#meal = string, type of meal ex: Breakfast, Lunch, and Dinner
class MealPlanModification():
    @staticmethod
    def AddToMealPlan(name, day, meal):
        comp = day + ":\n"
        compMeal = "-" + meal + "\n"
        mealPlan = open("display/MealPlanTemplate.txt", "r")
        fileContent = mealPlan.readlines()
        correctDay = False
        correctMeal = False
    
        i = 0
        while i < len(fileContent) - 1:
            if fileContent[i] == comp:
                correctDay = True
                correctMeal = False
        
            if fileContent[i] == compMeal:
                correctMeal = True

            if correctDay and correctMeal:
                fileContent[i+1] = name + "\n"
                correctDay = False
                correctMeal = False
            i += 1

        mealPlan.close()
    
        mealPlan = open("display/MealPlanTemplate.txt", "w")
        mealPlan.writelines(fileContent)
        mealPlan.close()

class FindRecipeDetailsForOneRecipe ():
    @staticmethod
    def FindSingleDetails(recipe):
        with open('display/DataBase.txt') as f:
            for line in f:
            
                if recipe in line:
                    ingredients = next(f).strip('& ')
                    cost = next(f).strip('$ ')
                    instructions = next(f).strip(': ')
                    return [recipe,cost.strip('\n'),ingredients.strip('\n'),instructions.strip('\n')]

#Developed by Ikaika Lee
#Class to find the details of the returned recipes based on the user's input
class FindRecipeDetails():
    @staticmethod
    def FindRecipe(recipes):
        i = 0
        read = open("display/DataBase.txt", "r")
        for line in read:
            if '*' in line:
                if line.strip('* ').strip('\n') in recipes[i] and i < 5: #checks to see if the current line in the database matches a recipe in the list and makes sure it is only checking the top 3 results
                    outputDetails = open('display/Output.txt', 'a')
                    outputDetails.write(line.strip('* ')) #strip the key symbol off the recipe's name in the database
                    outputDetails.write(next(read).strip('& ')) #strip the key symbol off the recipe's ingredients in the database
                    outputDetails.write(next(read).strip('$ ')) #strip the key symbol off the recipe's price in the database
                    outputDetails.write(next(read).strip(': ')) #strip the key symbol off the recipe's steps in the database
                    outputDetails.write('\n')
                    outputDetails.close()
                    read.seek(0,0) #reposition position in database to the top
                    i += 1 #incrimenting as a recipe is found
        read.close()

#Developed by Ikaika Lee
#Class to add submitted recipes to the database
class RecipeSubmissionOutput():
    @staticmethod
    def writeInFile(cost, name, ingredients, direction):
        recipeSubmit = open("display/DataBase.txt", "a")
        recipeSubmit.write('\n* ')
        recipeSubmit.write(name)
        recipeSubmit.write('\n& ')
        recipeSubmit.write(ingredients)
        recipeSubmit.write("\n$ ")
        recipeSubmit.write(cost)
        recipeSubmit.write("\n: ")
        recipeSubmit.write(direction)
        recipeSubmit.close()

#developed by Anthony Vuong
class SearchEngine():
    __recipes = [] #list of recipes names
    __hits = [] #associated list with __recipes with each index containing a number denoting the correlating recipe's relevance
    
    
    def __init__(self):       


        #default filter settings
        self._price = 'none'
        self._name = 'none'
        self._ingredients = []
        
        #default filter initialization
        self._nameFilter = NameFilter(self._name)
        self._priceFilter = PriceFilter(self._price)
        self._ingredientsFilter = IngredientFilter(self._ingredients)

        
    #changes price key
    def changePrice(self, price):

        self._price = price
        self._priceFilter.changeKey(price)
        
    #changes Name key
    def changeName(self, Name):

        self._name = Name
        self._nameFilter.changeKey(Name)
        
    #adds ingredient to ingredients list
    def addIngredients(self, ingredients):

        self._ingredients = ingredients.split(",")
        self._ingredientsFilter.changeKey(ingredients.split(","))
   

    #initializes the filters for searching
    def __newNameFilter(self):
        self._nameFilter = NameFilter(self._name)

    def __newPriceFilter(self):
        self._priceFilter = PriceFilter(self._price)

    def __newIngredientFilter(self):
        self._ingredientsFilter = IngredientFilter(self._ingredients)
        
    #delete Keys
    def deleteName(self):
        self._nameFilter.delKey()

    def deletePrice(self):
        self._priceFilter.delKey()

    def deleteAllIngredients(self):
       self._ingredientsFilter.delKey()

    def deleteIngredient(self, ingredient):
       self._ingredientsFilter.delIngredient(ingredient)
    
    
    #Search method
    def searchFilters(self):
        
        #resets weight lists
        self.__recipes = []
        self.__hits = []
        
        #searches through the recipe database and looks for special symbols that denote the type of information on that line
        file = open('display/DataBase.txt', 'r')
        
        i=-1    #keeps track of what recipe we are on
       
        for line in file:
            
            if '*' in line: #name symbol
                i += 1
                self.__recipes.append(line.strip('* ').strip('\n'))
                self.__hits.append(0)
                self.__hits[i] = self._nameFilter.search(line, self.__hits[i])

            if '$' in line: #price symbol
                self.__hits[i] = self._priceFilter.search(line, self.__hits[i])

            if '&' in line: #ingredient symbol
                self.__hits[i] = self._ingredientsFilter.search(line, self.__hits[i])                  
        file.close()
        
        #sorts our list using the weight list
        self.insertionSort()
        self.hideRecipes()
        return self.__recipes   #returns sorted __recipes list 
    

    #modified insertion sort for our purposes
    def insertionSort(self): 
  
        for i in range(1, len(self.__hits)): 
      
            key = self.__hits[i]
            ikey = self.__recipes[i]
      
            j = i-1
            while j >=0 and key > self.__hits[j] : 
                    self.__hits[j+1] = self.__hits[j]
                    self.__recipes[j+1] = self.__recipes[j]
                    j -= 1
            self.__hits[j+1] = key
            self.__recipes[j+1] = ikey

    #deletes recipes with no weight
    def hideRecipes(self):
        
        for i in range(len(self.__hits)):
            if self.__hits[len(self.__hits)-i-1] == 0:
                del self.__recipes[len(self.__hits)-i-1]
        
    #print stuffs
    def printEverything(self):
        self._nameFilter.showKey()
        self._priceFilter.showKey()
        self._ingredientsFilter.showKey()
