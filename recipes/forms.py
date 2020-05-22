from django import forms
from django.forms import ModelForm
from .models import Recipe


# class RecipeForm(ModelForm):
# 	class Meta:
# 		model = Recipe
# 		fields = ['name', 'photo', 'author']

class RecipeForm(forms.Form):
	name = forms.CharField(label='Recipe name', max_length=200)
	photo = forms.URLField(label='Photo URL', max_length=400, required=False)
	author = forms.CharField(label='Your name', max_length=100)
	# forms.
