# Generated by Django 5.0.3 on 2024-06-14 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cookingweb', '0012_alter_profile_avatar_alter_profile_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='recipe',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='comment',
        ),
        migrations.DeleteModel(
            name='Collection',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
