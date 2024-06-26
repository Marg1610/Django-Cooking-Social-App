# Generated by Django 5.0.3 on 2024-05-23 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cookingweb', '0009_alter_rating_options_alter_tag_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['tag_type__name', 'name'], 'verbose_name': 'Тег', 'verbose_name_plural': 'Теги'},
        ),
        migrations.AlterModelOptions(
            name='tagtype',
            options={'ordering': ['name'], 'verbose_name': 'Тип тега', 'verbose_name_plural': 'Типы тегов'},
        ),
        migrations.RemoveField(
            model_name='tagtype',
            name='group',
        ),
    ]
