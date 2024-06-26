# Generated by Django 5.0.3 on 2024-04-13 07:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cookingweb', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelOptions(
            name='rating',
            options={'verbose_name': 'Оценки', 'verbose_name_plural': 'Оценки'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-publication_date'], 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'Тег', 'verbose_name_plural': 'Теги'},
        ),
        migrations.AlterModelOptions(
            name='tagtype',
            options={'verbose_name': 'Тип тега', 'verbose_name_plural': 'Типы тегов'},
        ),
    ]
