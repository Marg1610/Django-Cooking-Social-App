from random import choices
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.core.exceptions import ValidationError
import uuid

COLOR_CHOICES = (
    ('white', 'Белый'),
    ('red', 'Красный'),
    ('orange', 'Оранжевый'),
    ('yellow', 'Желтый'),
    ('green', 'Зеленый'),
    ('lightblue', 'Голубой'),
    ('blue', 'Синий'),
    ('purple', 'Фиолетовый'),
    ('pink', 'Розовый'),
    ('brown', 'Коричневый'),
    ('gray', 'Серый'),
)
    
class TagType(models.Model):
    # Типы тегов
    name = models.CharField('Имя типа', max_length=50, unique=True)
    color = models.CharField('Цвет тега', max_length=10, choices=COLOR_CHOICES, default='white')
    multiple_choice = models.BooleanField('Множественный выбор', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип тега'
        verbose_name_plural = 'Типы тегов'
        ordering = ['name']
    
class Tag(models.Model):
    # Тег
    name = models.CharField('Имя тега', max_length=50, unique=True)
    tag_type = models.ForeignKey(TagType, verbose_name='Тип', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['tag_type__name', 'name']
   
class Recipe(models.Model):
    # Рецепт
    author = models.ForeignKey(User, verbose_name='Автор публикации', on_delete=models.CASCADE)
    title = models.CharField('Название рецепта', max_length=200)
    description = models.TextField('Описание', default='')
    cooking_time=models.PositiveIntegerField('Время приготовления', default=10)
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    image = models.ImageField('Изображение', upload_to='recipes/', default='recipes/no_image.png')
    publication_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    draft = models.BooleanField('Черновик', default=False)
    content = RichTextField('Содержание', default='')
    favorited_by = models.ManyToManyField(User, verbose_name='В избранном', related_name='favorite_recipes')

    def get_rating(self):
        likes_count = self.rating_set.filter(value=Rating.LIKE).count()
        dislikes_count = self.rating_set.filter(value=Rating.DISLIKE).count()
        return likes_count - dislikes_count
    
    def get_favorites_count(self):
        return self.favorited_by.count()
    def clean(self):
        if self.pk:
            favorited_users = self.favorited_by.all()
            for user in favorited_users:
                if user in self.favorited_by.filter(pk=self.pk):
                    raise ValidationError('Рецепт уже добавлен в избранное')
        else:
            pass

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-publication_date']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.pk:
            old_recipe = Recipe.objects.get(pk=self.pk)
            if old_recipe.image == self.image:
                super(Recipe, self).save(*args, **kwargs)
                return
            else:
                old_image = old_recipe.image
        else:
            old_image = None

        if self.image:
            self.image.name = f'{uuid.uuid4()}.{self.image.name.split(".")[-1]}'

        super(Recipe, self).save(*args, **kwargs)

        if old_image:
            old_image.delete(save=False)

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super(Recipe, self).delete(*args, **kwargs)

class Rating(models.Model):
    # Оценка
    LIKE = 1
    DISLIKE = -1
    RATING_CHOICES = [
        (LIKE, 'Нравится'),
        (DISLIKE, 'Не нравится'),
    ]
    value = models.IntegerField('Значение оценки', choices=RATING_CHOICES)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        unique_together = ('user', 'recipe',)
    


