"""Views for `recipes` app."""

# Reference for all CBV classes available:
# https://docs.djangoproject.com/en/3.1/ref/class-based-views/

from typing import Any

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models.query import QuerySet
from django.views.generic import DetailView, ListView

from .models import Recipe


class RecipeListView(ListView):
    """List view for Recipe collection."""

    model = Recipe
    context_object_name = "recipes"
    paginate_by = 10

    def get_queryset(self) -> QuerySet:
        """Add a search capacity to the list view."""
        qs = super().get_queryset()

        if not self.request.user.is_authenticated:
            # Remove private recipes from the results
            qs = qs.filter(is_private=False)

        query_term = self.request.GET.get("query")
        if query_term:
            # fmt: off
            vector = (
                SearchVector("title", weight="A")
                + SearchVector("subtitle", weight="A")
                + SearchVector("ingredients__ingredient_type__name", weight="A")
                + SearchVector("description", weight="B")
                + SearchVector("directions", weight="C")
                + SearchVector("footnotes", weight="D")
            )
            # fmt: on
            query = SearchQuery(query_term)
            qs = (
                qs.annotate(rank=SearchRank(vector, query))
                .filter(rank__gte=0.3)
                .distinct("id")
                .order_by("id", "-rank")
            )
        return qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["search_term"] = self.request.GET.get("query")
        count_qs = self.model.objects.all()
        if not self.request.user.is_authenticated:
            # Count only public recipes.
            # Counting all would be a data leak.
            count_qs = count_qs.filter(is_private=False)
        context["all_recipes_count"] = count_qs.count()
        return context


class RecipeDetailView(DetailView):
    """Detail view for a Recipe instance."""

    context_object_name = "recipe"

    def get_queryset(self) -> QuerySet:
        qs = Recipe.objects.prefetch_related(
            "ingredients",
            "ingredient_sections__sectioned_ingredients",
        )
        if not self.request.user.is_authenticated:
            # Filter out private recipes.
            # The view will naturally throw a 404 error when a non-auth user
            # tries to access a private recipe in some way.
            # TODO create a nifty-looking 404 page
            qs = qs.filter(is_private=False)
        return qs
