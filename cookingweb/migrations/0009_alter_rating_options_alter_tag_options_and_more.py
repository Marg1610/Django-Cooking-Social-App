# Generated by Django 5.0.3 on 2024-05-23 08:27

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookingweb', '0008_tagtype_multiple_choice_alter_recipe_cooking_time_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rating',
            options={'verbose_name': 'Оценка', 'verbose_name_plural': 'Оценки'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['tag_type__group', 'tag_type__name', 'name'], 'verbose_name': 'Тег', 'verbose_name_plural': 'Теги'},
        ),
        migrations.AlterModelOptions(
            name='tagtype',
            options={'ordering': ['group', 'name'], 'verbose_name': 'Тип тега', 'verbose_name_plural': 'Типы тегов'},
        ),
        migrations.AddField(
            model_name='recipe',
            name='favorited_by',
            field=models.ManyToManyField(related_name='favorite_recipes', to=settings.AUTH_USER_MODEL, verbose_name='В избранном'),
        ),
        migrations.AddField(
            model_name='tagtype',
            name='group',
            field=models.CharField(default='', max_length=50, verbose_name='Группа'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='content',
            field=ckeditor.fields.RichTextField(default='', verbose_name='Содержание'),
        ),
        migrations.DeleteModel(
            name='Favorite',
        ),
    ]
