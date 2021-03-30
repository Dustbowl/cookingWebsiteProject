from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import MealPlanModification, FindRecipeDetailsForOneRecipe, FindRecipeDetails, SearchToolForm, RecipeSubmissionForm, MealPlanForm, SearchEngine, RecipeSubmissionOutput
import shutil
#import re
from .meal_plan import daily_plan, daily_meals
#from .SearchEngine import SearchEngine

def Homepage(request):
    return render(request,'display/homepage.html/')

def SearchTool(request):
    form = SearchToolForm(request.POST or None)
    f = open("display/Output.txt", "a")
    f.truncate(0)
    f.write('')
    f.close()
    if request.method == 'POST':
        if form.is_valid():
            price_range = form['price_filter'].data
            name = form['name'].data
            ingredients = form['ingredients'].data
            amountRecipes = form['amountRecipes'].data

            if price_range == 'under_5': #if else statement to convert button value into integer to be compared in the price filter
                price_range = 5
            elif price_range == '5_10':
                price_range = 10
            else:
                price_range = 15

            obj = SearchEngine()
            obj.changePrice(price_range)
            obj.changeName(name)
            obj.addIngredients(ingredients)
            obj.printEverything()
            recipes = obj.searchFilters()

            all_recipe_details = []
            details = FindRecipeDetails()
            details.FindRecipe(recipes, amountRecipes)
            detailsForOne = FindRecipeDetailsForOneRecipe()

            for i in range (0,int(float(amountRecipes))):
                all_recipe_details.append(detailsForOne.FindSingleDetails(recipes[i]))
            
            
            return render(request,'display/search_tool.html/', {
                'form': form,
                'recipes': json.dumps(all_recipe_details),
                'downloadable': 1,
            })
    
    return render(request,'display/search_tool.html/', {
        'form':form
    })

def RecipeSubmission(request):
    form = RecipeSubmissionForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            cost = form['cost'].data
            name = form['name'].data
            ingredients = form['ingredients'].data
            direction = form['direction'].data
            obj = RecipeSubmissionOutput()
            obj.writeInFile(cost, name, ingredients, direction)
            return render(request,'display/recipe_submission.html/', {
                'form':form,
                'success_msg': 1,
            })
    return render(request,'display/recipe_submission.html/', {
        'form':form
    })

#developed by Jacob Dickson and Ikaika Lee
def MealPlan(request):
    form = MealPlanForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            name = form['name'].data
            day = form['day'].data
            meal = form['meal'].data
            obj = MealPlanModification()
            obj.AddToMealPlan(name, day, meal)
            total = day+meal
            daily_meals[total] = name
            
            return render(request, 'display/meal_plan.html/', {
                'form': form,
                'monBreakfast': daily_meals['MondayBreakfast'],
                'monLunch': daily_meals['MondayLunch'],
                'monDinner': daily_meals['MondayDinner'],
                'tueBreakfast': daily_meals['TuesdayBreakfast'],
                'tueLunch': daily_meals['TuesdayLunch'],
                'tueDinner': daily_meals['TuesdayDinner'],
                'wedBreakfast': daily_meals['WednesdayBreakfast'],
                'wedLunch': daily_meals['WednesdayLunch'],
                'wedDinner': daily_meals['WednesdayDinner'],
                'thuBreakfast': daily_meals['ThursdayBreakfast'],
                'thuLunch': daily_meals['ThursdayLunch'],
                'thuDinner': daily_meals['ThursdayDinner'],
                'friBreakfast': daily_meals['FridayBreakfast'],
                'friLunch': daily_meals['FridayLunch'],
                'friDinner': daily_meals['FridayDinner'],
                'satBreakfast': daily_meals['SaturdayBreakfast'],
                'satLunch': daily_meals['SaturdayLunch'],
                'satDinner': daily_meals['SaturdayDinner'],
                'sunBreakfast': daily_meals['SundayBreakfast'],
                'sunLunch': daily_meals['SundayLunch'],
                'sunDinner': daily_meals['SundayDinner'],
                'downloadable': 1,
            })
    f = open("display/MealPlanTemplate.txt", "a")
    f.truncate(0)
    f.write("Monday:\n-Breakfast\n\n-Lunch\n\n-Dinner\n\n")
    f.write("Tuesday:\n-Breakfast\n\n-Lunch\n\n-Dinner\n\n")
    f.write("Wednesday:\n-Breakfast\n\n-Lunch\n\n-Dinner\n\n")
    f.write("Thursday:\n-Breakfast\n\n-Lunch\n\n-Dinner\n\n")
    f.write("Friday:\n-Breakfast\n\n-Lunch\n\n-Dinner\n\n")
    f.write("Saturday:\n-Breakfast\n\n-Lunch\n\n-Dinner\n\n")
    f.write("Sunday:\n-Breakfast\n\n-Lunch\n\n-Dinner\n\n")
    f.close()
    
def GetTextFile(request):
    return render(request, 'display/Output.txt')

def Help(request):
    return render(request,'display/help.html/')


def GetTextFile(request):
    file_name = request.GET.get('file_name')
    with open('display/{}.txt'.format(file_name), 'r') as file:
        output = file.read()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}.txt"'.format(file_name)
    response.write(output)
    return response
