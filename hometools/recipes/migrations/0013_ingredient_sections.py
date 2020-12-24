# Generated by Django 3.1.4 on 2020-12-24 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0012_auto_20201126_1233"),
    ]

    operations = [
        migrations.CreateModel(
            name="IngredientSection",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "time_created",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="created"
                    ),
                ),
                (
                    "time_modified",
                    models.DateTimeField(
                        auto_now=True, db_index=True, verbose_name="modified"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        help_text="Name of this section of Ingredients, used as the section title when displayed on the frontend.",
                        max_length=255,
                    ),
                ),
                ("order", models.PositiveIntegerField(default=0)),
                (
                    "recipe",
                    models.ForeignKey(
                        help_text="The Recipe this section of Ingredients belongs to",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ingredient_sections",
                        to="recipes.recipe",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="recipeingredient",
            name="section",
            field=models.ForeignKey(
                blank=True,
                help_text="Section of ingredients that this Ingredient falls under.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="sectioned_ingredients",
                to="recipes.ingredientsection",
            ),
        ),
    ]
