from django.urls import include, path

from .views import (DownloadShoppingCart,
                    IngredientViewSet,
                    RecipeViewSet, TagViewSet)

from rest_framework.routers import DefaultRouter


app_name = 'api'

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('recipes/download_shopping_cart/',
         DownloadShoppingCart.as_view(), name='download'),
    path('', include(router.urls)),
    # path('recipes/<int:favorite_id>/favorite/', FavoriteApiView.as_view()),
    # path('recipes/<int:recipe_id>/shopping_cart/', ShoppingView.as_view()),
]
