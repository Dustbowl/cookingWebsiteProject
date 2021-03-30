from django.db import models
from django import forms
from .Filter import Filter
from .PriceFilter import PriceFilter
from .NameFilter import NameFilter
from .IngredientFilter import IngredientFilter

# models.py includes classes and forms

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

#class Filter:

#    def __init__(self, key):

#        self._key = key
        #key is the keyword being used to search

#    def showKey(self):
#        print(self._key)
        
    #def delKey(self):

    #    self._key = 'none'

    #def changeKey(self, key):

    #    self._key = key
        
class MealPlanForm (forms.Form):
    name = forms.CharField(label="Meal Name")
    day = forms.CharField(label='Day', widget=forms.Select(choices= days))
    meal = forms.CharField(label='Meal', widget=forms.Select(choices= meals))


# Developed by Khanh Vu
# A form where user can look up recipe by selecting price_filter from a dropdown menu and 
# inputting name and ingredients in textboxes 
# None of the fields are required in this form.
class SearchToolForm (forms.Form):
    price_filter = forms.CharField(widget=forms.Select(choices=price_range), required=False)
    name = forms.CharField(label="Name", required=False)
    ingredients = forms.CharField(label="Ingredients",widget=forms.Textarea(), required=False)


# Developed by Khanh Vu
# A form where user can submit a recipe. 
# All fields, including cost, name, ingredients, direction are required in this form.
class RecipeSubmissionForm (forms.Form):
    #cost = forms.CharField(widget=forms.Select(choices=price_range))
    cost = forms.CharField(label="Cost")
    name = forms.CharField(label="Name")
    ingredients = forms.CharField(label="Ingredients",widget=forms.Textarea())
    direction = forms.CharField(label="Direction",widget=forms.Textarea())

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
