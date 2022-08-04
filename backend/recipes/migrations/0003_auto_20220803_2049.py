# Generated by Django 2.2.16 on 2022-08-03 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20220803_1953'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['-id'], 'verbose_name': 'Тег', 'verbose_name_plural': 'Теги'},
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]