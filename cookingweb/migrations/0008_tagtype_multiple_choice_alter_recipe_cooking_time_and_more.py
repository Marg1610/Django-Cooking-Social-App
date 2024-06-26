# Generated by Django 5.0.3 on 2024-05-17 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookingweb', '0007_alter_recipe_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='tagtype',
            name='multiple_choice',
            field=models.BooleanField(default=True, verbose_name='Множественный выбор'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(default=10, verbose_name='Время приготовления'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default='recipes/no_image.png', upload_to='recipes/', verbose_name='Изображение'),
        ),
    ]
