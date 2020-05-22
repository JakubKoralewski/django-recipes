from typing import Dict
import json
from ..models import Recipe, StepToBeAdded, IngredientsOfStep, IngredientToBeAdded, StepsOfRecipe, Author
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from http import HTTPStatus


@csrf_exempt
def new(request):
	if request.method != "POST":
		return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)
	jsondata: Dict
	try:
		jsondata = json.loads(request.body)
	except:
		return HttpResponse(status=HTTPStatus.BAD_REQUEST, content='json structure invalid')
	try:
		recipe_name = jsondata['name'].strip()
	except KeyError:
		return HttpResponse(status=HTTPStatus.BAD_REQUEST, content='provide recipe name')
	try:
		recipe_author = jsondata['author'].strip()
	except KeyError:
		return HttpResponse(status=HTTPStatus.BAD_REQUEST, content='provide recipe author')

	try:
		stepsdata = jsondata['steps']
	except KeyError:
		return HttpResponse(status=HTTPStatus.BAD_REQUEST, content='provide recipe\'s steps')

	if not isinstance(stepsdata, list):
		return HttpResponse(status=HTTPStatus.BAD_REQUEST, content='steps should be a list')

	if len(stepsdata) == 0:
		return HttpResponse(status=HTTPStatus.BAD_REQUEST, content="steps can't be empty")

	steps = []

	for step in stepsdata:
		new_step = StepToBeAdded()
		try:
			new_step.description = step['description'].strip()
		except KeyError:
			return HttpResponse(status=HTTPStatus.BAD_REQUEST, content="each step must have description")

		new_ingredients = step.get('ingredients')
		if new_ingredients:
			if not isinstance(new_ingredients, list):
				return HttpResponse(status=HTTPStatus.BAD_REQUEST,
									content="ingredients of each step must be list if defined")
			new_ingredient = IngredientToBeAdded()
			for new_ing in new_ingredients:
				try:
					new_ingredient.set_field('name', new_ing['name'].strip())
				except KeyError:
					return HttpResponse(status=HTTPStatus.BAD_REQUEST,
										content="ingredient must have name")
				try:
					new_ingredient.set_field('type', new_ing['type'])
				except KeyError:
					return HttpResponse(status=HTTPStatus.BAD_REQUEST,
										content="ingredient must have type")
				try:
					new_ingredient.set_field('amount', new_ing['amount'])
				except KeyError:
					return HttpResponse(status=HTTPStatus.BAD_REQUEST,
										content="ingredient must have amount")
				try:
					new_ingredient.set_field('amount_type', new_ing['amount_type'].strip())
				except KeyError:
					return HttpResponse(status=HTTPStatus.BAD_REQUEST,
										content="ingredient must have amount_type")
				new_ingredient_photo = new_ing.get('photo', '')
				new_ingredient.set_field('photo', new_ingredient_photo)
				new_step.ingredients.append(new_ingredient)
		steps.append(new_step)

	recipe_photo = jsondata.get('photo')
	try:
		author = Author.objects.get(name__iexact=recipe_author)
	except Author.DoesNotExist:
		try:
			author = Author(name=recipe_author)
		except:
			return HttpResponse(status=HTTPStatus.BAD_REQUEST,
								content="invalid author name")
		author.save()
	try:
		new_recipe = Recipe(name=recipe_name, photo=recipe_photo, author=author)
	except Exception as e:
		return HttpResponse(status=HTTPStatus.BAD_REQUEST,
							content=f"invalid recipe data: {e}")

	new_recipe.save()
	new_recipe.add_steps(steps)

	return HttpResponse(status=HTTPStatus.OK, content=new_recipe.id)
