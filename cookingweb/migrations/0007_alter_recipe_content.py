# Generated by Django 5.0.3 on 2024-05-17 19:11

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cookingweb', '0006_recipe_content_alter_recipe_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='content',
            field=tinymce.models.HTMLField(default='', verbose_name='Содержание'),
        ),
    ]