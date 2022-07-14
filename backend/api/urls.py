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
    path('v1/recipes/download_shopping_cart/',
         DownloadShoppingCart.as_view(), name='download'),
    path('v1/', include(router.urls)),
]
