"""Views for `recipes` app."""
# TODO: fill in template details for best-practice with Class-Based Views.
# Starter: https://spapas.github.io/2018/03/19/comprehensive-django-cbv-guide/

# Reference for all CBV classes available:
# https://docs.djangoproject.com/en/3.1/ref/class-based-views/

from typing import (
    Any,
    Dict,
)

from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
)
from django.db.models.query import QuerySet
from django.views.generic import (
    ListView,
    DetailView,
)
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Recipe


class RecipeBaseViewMixin(PermissionRequiredMixin):
    permission_required = "recipes.view_recipe"
    login_url = "/login/"


class RecipeListView(RecipeBaseViewMixin, ListView):
    """List view for Recipe collection."""

    model = Recipe
    context_object_name = "recipes"
    paginate_by = 10

    def get_queryset(self) -> QuerySet:
        """Add a search capacity to the list view."""
        qs = super().get_queryset()
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

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["search_term"] = self.request.GET.get("query")
        context["all_recipes_count"] = self.model.objects.count()
        return context


class RecipeDetailView(RecipeBaseViewMixin, DetailView):
    """Detail view for a Recipe instance."""

    context_object_name = "recipe"
    queryset = Recipe.objects.prefetch_related(
        "ingredients",
        "ingredient_sections__sectioned_ingredients",
    )
