# Generated by Django 3.0.6 on 2020-05-22 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_auto_20200522_1001'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StepsOfRecipes',
            new_name='StepsOfRecipe',
        ),
    ]
