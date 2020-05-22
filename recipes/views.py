from typing import Dict

from django.http import HttpResponseRedirect
from django.views import generic
from django.shortcuts import render, get_object_or_404
from ipware import get_client_ip
from pprint import pprint

from .forms import RecipeForm
from .models import Recipe, StepsOfRecipe, IngredientsOfStep, IngredientToBeAdded, StepToBeAdded, IngredientType, \
	AmountType


class IndexView(generic.ListView):
	# https://docs.djangoproject.com/en/3.0/intro/tutorial04/
	template_name = 'recipes/index.html'
	context_object_name = 'latest_recipes'

	def get_queryset(self):
		"""Return the last five published questions."""
		return Recipe.objects.order_by('-pub_date')[:5]


# https://docs.djangoproject.com/en/3.0/intro/tutorial03/
# def index(request):
# 	latest_recipes = Recipe.objects.order_by('-pub_date')[:5]
# 	context = {
# 		'latest_recipes': latest_recipes
# 	}
# https://docs.djangoproject.com/en/3.0/ref/request-response/

def detail(request, recipe_id):
	ip, is_routable = get_client_ip(request)
	# https://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
	print(f'ip: "{ip}"')
	client_name = None
	if is_routable:
		client_name = ip
		if '.'.join(ip.split(".")[:3]) == '150.254.76':
			client_name = 'Hello teacher :)'
	else:
		client_name = ip

	recipe = get_object_or_404(Recipe, pk=recipe_id)
	raw_steps = StepsOfRecipe.objects.filter(recipe_id=recipe_id)
	steps = []
	for s in raw_steps:
		steps.append({'step': s, 'ingredients': IngredientsOfStep.objects.filter(step_id=s.id)})
	context = {
		'recipe': recipe,
		'steps': steps,
		'about_user': client_name,
	}
	return render(request, 'recipes/detail.html', context)


def new(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = RecipeForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			print("form of new recipe: ")
			pprint(form.__dict__)
			new_recipe = Recipe.from_form(
				name=form.cleaned_data['name'],
				photo=form.cleaned_data['photo'],
				author=form.cleaned_data['author']
			)
			data = form.data
			parsed_data = parse_data(data)
			new_recipe.save()
			new_recipe.add_steps(parsed_data)
			# redirect to a new URL:
			return HttpResponseRedirect(f'/recipes/{new_recipe.id}')

	# if a GET (or any other method) we'll create a blank form
	else:
		form = RecipeForm()
	ingredient_types = IngredientType.choices
	amount_types = AmountType.choices
	context = {'form': form, 'ingredient_types': ingredient_types, 'amount_types': amount_types}

	return render(request, 'recipes/new.html', context)


def parse_data(data):
	parsed_data: Dict[int, StepToBeAdded] = {}
	for key in data:
		key: str
		index = -1
		if key.startswith('step-'):
			index_str = key[len('step') + 1:]
			index = int(index_str[:index_str.find('-')])
			if not parsed_data.get(index):
				parsed_data[index] = StepToBeAdded()
			step_field = key[len('step') + len(str(index)) + 2:]
			if step_field.startswith('ingredient'):
				last_dash_index = key.rfind('-')
				ingredient_index = int(key[last_dash_index:])
				ingredient_field = key[len('step') + len(str(index)) + 2 + len('ingredient') + 1:last_dash_index]
				if parsed_data[index].ingredients.get(ingredient_index):
					parsed_data[index].ingredients[ingredient_index].set_field(ingredient_field, data[key].strip())
				else:
					new_ing = IngredientToBeAdded()
					new_ing.set_field(ingredient_field, data[key].strip())
					parsed_data[index].ingredients[ingredient_index] = new_ing
			else:
				assert step_field == 'description'
				parsed_data[index].description = data[key].strip()
	for key in parsed_data:
		parsed_data[key].ingredients = parsed_data[key].ingredients.values()
	return parsed_data.values()
