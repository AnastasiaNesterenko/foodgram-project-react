# Generated by Django 2.2.16 on 2022-08-03 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(blank=True, choices=[('#0000FF', 'Синий'), ('#FFA500', 'Оранжевый'), ('#008000', 'Зеленый'), ('#800080', 'Фиолетовый'), ('#FFFF00', 'Желтый')], max_length=7, null=True, unique=True, verbose_name='Цвет тега'),
        ),
    ]
