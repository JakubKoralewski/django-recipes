from typing import List, Dict, Union

from django.db import models


# Create your models here.
# https://en.wikipedia.org/wiki/Cooking_weights_and_measures

class AmountType(models.TextChoices):
	GRAMS = ('g', 'grams')
	KILOGRAMS = ('kg', 'kilograms')
	MILLILITERS = ('ml', 'milliliters')
	TABLE_SPOONS = ('tbsp', 'tablespoons')
	TEA_SPOONS = ('tsp', 'teaspoons')
	COUNT = ('x', 'items')


class Author(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return f'Author: "{self.name}"'


class IngredientType(models.IntegerChoices):
	DAIRY_PRODUCT = (0, 'Dairy product')
	VEGETABLE = (1, 'Vegetable')
	FRUIT = (2, 'Fruit')
	MEAT = (3, 'Meat')
	FLOUR_LIKE = (4, 'Flour-like')
	RICE_LIKE = (5, 'Rice-like')
	OTHER = (100, 'Unknown')


class Ingredient(models.Model):
	name = models.CharField(max_length=200)
	photo = models.URLField(max_length=400)
	type = models.IntegerField(choices=IngredientType.choices, default=IngredientType.OTHER)

	def __str__(self):
		return f'Ingredient: "{self.name}"'


class IngredientToBeAdded:
	name: str
	amount: Union[float, int]
	amount_type: str
	photo: str
	type: int  # cuz choices are ints

	def __str__(self):
		return ','.join(self.__dict__.items())

	def set_field(self, key: str, val):
		key = key.lower()
		if key == 'name':
			if not isinstance(val, str):
				raise Exception('name should be str')
			self.name = val
		elif key == 'photo':
			if not isinstance(val, str):
				raise Exception('photo should be str')
			self.photo = val
		elif key == 'amount':
			if not isinstance(val, int) and not isinstance(val, float):
				try:
					val = float(val)
				except:
					raise Exception('amount of ingredient should be number')
			self.amount = val
		elif key == 'amount_type':
			if not isinstance(val, str):
				raise Exception('amount type should be string')
			self.amount_type = val
		elif key == 'type':
			if not isinstance(val, int):
				try:
					val = int(val)
				except:
					raise Exception('type of ingredient should be int')
			self.type = val
		else:
			raise Exception(f'Unknown ingredient field tried to be saved: "{key}" of value: "{val}"')


class StepToBeAdded:
	description: str
	photo: str
	ingredients: List[IngredientToBeAdded]

	def __init__(self):
		self.ingredients = []

	def __str__(self):
		return ','.join(self.__dict__.items())


class Recipe(models.Model):
	name = models.CharField(max_length=200)
	photo = models.URLField(max_length=400, null=True, blank=True)
	author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
	pub_date = models.DateTimeField(auto_now_add=True, editable=False, help_text='Published date')
	votes = models.PositiveIntegerField(default=0)
	steps = models.PositiveIntegerField(default=0)

	@classmethod
	def from_form(cls, name: str, photo: str, author: str):
		self = Recipe(name=name, photo=photo)
		try:
			maybe_existing_author = Author.objects.get(name__iexact=author)
			self.author = maybe_existing_author
		except Author.DoesNotExist:
			new_author = Author(name=author)
			new_author.save()
			self.author = new_author
		return self

	def add_steps(self, steps: Union[List[StepToBeAdded]]):
		if isinstance(steps, list):
			for step in steps:
				self.add_step(step)
		elif isinstance(steps, dict):
			for step in steps.values():
				self.add_step(step)
		else:
			raise Exception("invalid type of steps added to recipes")

	def add_step(self, step: StepToBeAdded):
		if not self.id:
			raise Exception('Add the Recipe to the database before inserting steps!')
		new_step = StepsOfRecipe(recipe=self, step_amt=self.steps, description=step.description)
		new_step.save()
		self.steps += 1
		self.save()
		for ing in step.ingredients:
			ingredient: Ingredient
			try:
				maybe_ingredient = Ingredient.objects.get(name__iexact=ing.name)
				ingredient = maybe_ingredient
			except Ingredient.DoesNotExist:
				new_ingredient = Ingredient(name=ing.name, photo=ing.photo, type=ing.type)
				new_ingredient.save()
				ingredient = new_ingredient
			step_ing = IngredientsOfStep(
				step=new_step,
				ingredient=ingredient,
				amount=ing.amount,
				amount_type=ing.amount_type
			)
			step_ing.save()

	def __str__(self):
		return f'Recipe: name="{self.name}" author="{self.author.name if self.author else "no author"}"'


class StepsOfRecipe(models.Model):
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
	step_amt = models.PositiveIntegerField(default=0)
	description = models.TextField()

	def __str__(self):
		return f'{self.step_amt + 1}-th step of {self.recipe.name}'


class IngredientsOfStep(models.Model):
	step = models.ForeignKey(StepsOfRecipe, on_delete=models.CASCADE)
	ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
	amount = models.DecimalField(decimal_places=1, max_digits=100)
	amount_type = models.CharField(max_length=10, choices=AmountType.choices, default=AmountType.COUNT)

	def __str__(self):
		return f"Ingredient of {self.ingredient.name}'s {self.step.step_amt + 1}-th step"
