from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (DownloadShoppingCart, FavoriteRecipeApiView,
                    IngredientViewSet, ShoppingApiView,
                    RecipeViewSet, TagViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('v1/recipes/download_shopping_cart/',
         DownloadShoppingCart.as_view()),
    path(r'v1/recipes/<int:recipe_id>/favorite/',
         FavoriteRecipeApiView.as_view()),
    path(r'v1/recipes/<int:recipe_id>/shopping_cart/',
         ShoppingApiView.as_view()),
    path('v1/', include(router.urls)),
]
