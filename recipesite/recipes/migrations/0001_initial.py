# Generated by Django 3.1.2 on 2020-10-19 00:24

import django.db.models.deletion
import djfractions.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="IngredientType",
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
                        auto_now_add=True,
                        db_index=True,
                        verbose_name="created",
                    ),
                ),
                (
                    "time_modified",
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        verbose_name="modified",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Recipe",
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
                        auto_now_add=True,
                        db_index=True,
                        verbose_name="created",
                    ),
                ),
                (
                    "time_modified",
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        verbose_name="modified",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("time_to_prep", models.DurationField(blank=True, null=True)),
                ("time_to_cook", models.DurationField(blank=True, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="RecipeIngredient",
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
                        auto_now_add=True,
                        db_index=True,
                        verbose_name="created",
                    ),
                ),
                (
                    "time_modified",
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        verbose_name="modified",
                    ),
                ),
                (
                    "amount",
                    djfractions.models.fields.DecimalFractionField(
                        coerce_thirds=True,
                        decimal_places=2,
                        limit_denominator=None,
                        max_digits=5,
                    ),
                ),
                ("amount_uom", models.CharField(max_length=5)),
                (
                    "ingredient_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="recipes.ingredienttype",
                    ),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="recipes.recipe",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="recipe",
            name="ingredients",
            field=models.ManyToManyField(
                through="recipes.RecipeIngredient",
                to="recipes.IngredientType",
            ),
        ),
    ]
