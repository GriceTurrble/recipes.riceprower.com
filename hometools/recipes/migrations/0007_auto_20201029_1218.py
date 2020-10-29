# Generated by Django 3.1.2 on 2020-10-29 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0006_auto_20201028_1136"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="recipeingredient",
            options={"ordering": ["order"], "verbose_name": "Ingredient"},
        ),
        migrations.AlterField(
            model_name="recipeingredient",
            name="amount_uom",
            field=models.CharField(
                choices=[
                    ("blank", "(blank)"),
                    ("cup", "cup"),
                    ("dash", "dash"),
                    ("fluid-ounce", "fluid ounce"),
                    ("fuckton", "fuckton"),
                    ("gallon", "gallon"),
                    ("gram", "gram"),
                    ("kilogram", "kilogram"),
                    ("liter", "liter"),
                    ("ml", "ml"),
                    ("pinch", "pinch"),
                    ("pint", "pint"),
                    ("pound", "pound"),
                    ("quart", "quart"),
                    ("tbsp", "tablespoon"),
                    ("tsp", "teaspoon"),
                    ("weight-ounce", "ounce"),
                ],
                default="blank",
                help_text="Unit of measure for 'amount'.",
                max_length=20,
            ),
        ),
    ]
