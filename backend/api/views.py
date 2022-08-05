from django.db.models import Sum
from django.shortcuts import HttpResponse, get_object_or_404

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from rest_framework import viewsets, views, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import AuthorAndTagFilter, IngredientSearchFilter
from .pagination import CustomPageNumberPagination
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (FavoriteRecipeSerializer,
                          IngredientSerializer, RecipeListSerializer,
                          RecipeSerializer, TagSerializer)
# from .serializers import (CartSerializer, FavoriteRecipeSerializer,
#                           IngredientSerializer, RecipeListSerializer,
#                           RecipeSerializer, TagSerializer)
from recipes.models import (FavoriteRecipe, Ingredient, Recipe,
                            IngredientAmount, Cart, Tag)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (IsOwnerOrReadOnly,)
    filter_class = AuthorAndTagFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeSerializer

    @staticmethod
    def post_method_for_actions(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_method_for_actions(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_obj = get_object_or_404(model, user=user, recipe=recipe)
        model_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["POST"],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=FavoriteRecipeSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=FavoriteRecipe)

    # @action(detail=True, methods=["POST"],
    #         permission_classes=[IsAuthenticated])
    # def shopping_cart(self, request, pk):
    #     return self.post_method_for_actions(
    #         request=request, pk=pk, serializers=CartSerializer)

    @action(detail=True, methods=['get', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        if request.method == 'GET':
            return self.add_obj(Cart, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_obj(Cart, request.user, pk)
        return None

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=Cart)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [IngredientSearchFilter]
    search_fields = ('^name',)
    pagination_class = None


class DownloadShoppingCart(views.APIView):
    permission_classes = (IsAuthenticated, )
    pagination_class = None

    def get(self, request):
        final_list = {}
        ingredients = IngredientAmount.objects.filter(
            recipe__cart__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(
            total=Sum('amount')).order_by('ingredient__name')
        for item in ingredients:
            name = item['ingredient__name']
            final_list[name] = {
                'measurement_unit': item['ingredient__measurement_unit'],
                'total': item['total']
            }
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
            page.drawString(75, height, (f'{i}. {name} - {data["total"]} '
                                         f'{data["measurement_unit"]}'))
            height -= 25
        page.showPage()
        page.save()
        return response
