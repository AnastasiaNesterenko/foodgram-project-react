from django.db.models import Sum
from django.shortcuts import HttpResponse, get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import filters,  viewsets, views, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from recipes.models import (FavoriteRecipe, Ingredient, Recipe,
                            IngredientAmount, Cart, Tag)
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (FavoriteRecipeSerializer, IngredientSerializer,
                          RecipeSerializer, CartSerializer,
                          TagSerializer)

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)


class FavoriteRecipeApiView(views.APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, recipe_id):
        user = request.user

        data = {
            'recipe': recipe_id,
            'user': user.id,
        }
        serializer = FavoriteRecipeSerializer(data=data,
                                        context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        FavoriteRecipe.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingApiView(views.APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, recipe_id):
        user = request.user
        data = {
            'recipe': recipe_id,
            'user': user.id
        }
        context = {'request': request}
        serializer = CartSerializer(data=data,
                                            context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        ShoppingCart.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DownloadShoppingCart(views.APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        final_list = {}
        # так тут же есть values_list или как-то по другому должно реализовываться? и с .annotate(total=Sum('amount')) не поняла
        ingredients = IngredientAmount.objects.filter(
             recipe__cart__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
            'amount'
        )
        for item in ingredients:
            name = item[0]
            if name not in final_list:
                final_list[name] = {
                    'measurement_unit': item[1],
                    'amount': item[2]
                }
            else:
                final_list[name]['amount'] += item[2]
        # final_list = '\n'.join([
        #     f'{ingredient["ingredients__name"]} - {ingredient["total"]} '
        #     f'{ingredient["ingredients__measurement_unit"]}'
        #     for ingredient in ingredients
        # ])
        pdfmetrics.registerFont(
            TTFont('RussianPunk', 'data/RussianPunk.ttf', 'UTF-8'))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_list.pdf"')
        page = canvas.Canvas(response)
        page.setFont('RussianPunk', size=24)
        page.drawString(200, 800, 'Список покупок')
        page.setFont('RussianPunk', size=16)
        height = 750
        for i, (name, data) in enumerate(final_list.items(), 1):
            page.drawString(75, height, (f'{i}. {name} - {data["amount"]} '
                                         f'{data["measurement_unit"]}'))
            height -= 25
        page.showPage()
        page.save()
        return response
