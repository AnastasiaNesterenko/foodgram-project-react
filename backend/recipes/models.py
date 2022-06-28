from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.dispatch import receiver

from users.models import User
from .validators import characters_validator


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название тега',
        blank=True
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Цвет тега',
        null=True,
        blank=True
    )
    slug = models.CharField(
        max_length=200,
        unique=True,
        null=True,
        blank=True,
        validators=[characters_validator]
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
        blank=True
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения ингредиента',
        blank=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}.'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
        blank=True
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        blank=True
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Изображение люда',
        blank=True,
        null=True
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        blank=True
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        through='RecipeIngredient',
        blank=True
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        help_text='Выберите тег',
        blank=True
    )
    cooking_time = models.IntegerField(
        help_text='Напишите время готовки в минутах',
        validators=[
            MinValueValidator(
                1,
                message='Время готовки не должно быть ниже 1'
            )
        ],
        blank=True,
        verbose_name='Время готовки',
    )

    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date', )

    def __str__(self):
        return f'{self.author.email}, {self.name}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Рецепт',
        blank=True
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='Ингредиент',
        blank=True
    )
    number = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(
                1,
                message='Количество продукта не может быть ниже 1'
            )
        ],
        verbose_name='Количество ингредиентов',
        blank=True
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique ingredient'
            )
        ]

    def __str__(self):
        return self.name


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites_user',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique favorite')
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique shopping cart')
        ]
