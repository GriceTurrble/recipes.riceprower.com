# Generated by Django 3.1.4 on 2020-12-25 01:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0013_ingredient_sections"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="ingredientsection",
            options={"ordering": ["order"], "verbose_name": "Ingredient Section"},
        ),
    ]