from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from .views import (DownloadShoppingCart, FavoriteRecipeApiView,
#                     IngredientViewSet, ShoppingApiView,
#                     RecipeViewSet, TagViewSet)
from .views import (IngredientViewSet,
                    RecipeViewSet, TagViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [
    # path('v1/recipes/download_shopping_cart/',
    #      DownloadShoppingCart.as_view(), name='download'),
    # path(r'v1/recipes/<int:recipe_id>/favorite/',
    #      FavoriteRecipeApiView.as_view(), name='favorite'),
    # path(r'v1/recipes/<int:recipe_id>/shopping_cart/',
    #      ShoppingApiView.as_view(), name='shopping_cart'),
    path('v1/', include(router.urls)),
]
