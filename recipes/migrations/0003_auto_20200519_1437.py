# Generated by Django 3.0.6 on 2020-05-19 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20200519_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientsofstep',
            name='amount_type',
            field=models.CharField(choices=[('g', 'grams'), ('kg', 'kilograms'), ('ml', 'milliliters'), ('tbsp', 'tablespoons'), ('tsp', 'teaspoons'), ('None', 'items')], default='None', max_length=10),
        ),
        migrations.AlterField(
            model_name='stepsofrecipes',
            name='used_ingredients',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='recipes.IngredientsOfStep'),
        ),
    ]
