from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Recipe, Tag, TagType, Rating
import re
from ckeditor.widgets import CKEditorWidget

def validate_username(value):
    value = value.lower()
    if len(value) < 3:
        raise forms.ValidationError('Имя пользователя должно содержать не менее 3 символов.')
    if not re.match(r'^[a-z][a-z0-9]*$', value):
        raise forms.ValidationError('Имя пользователя должно начинаться с буквы и содержать только латинские буквы и цифры.')

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label='Имя на сайте', required=False)
    username = forms.CharField(label='Логин', max_length=25, min_length=3,
                                validators=[validate_username],
                                help_text='Обязательное поле. Не более 25 символов и не менее 3. Только латинские буквы и цифры. Начинается с буквы.')
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name'] or user.username
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class RecipeCreateForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'cooking_time', 'tags', 'image', 'content']
        widgets = {
            'content': CKEditorWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(RecipeCreateForm, self).__init__(*args, **kwargs)

        self.fields.pop('tags')

        for tag_type in TagType.objects.all():
            tags = Tag.objects.filter(tag_type=tag_type)

            if tag_type.multiple_choice:
                # Флажки, если можно выбрать несколько тегов
                self.fields[f'tags_{tag_type.name}'] = forms.ModelMultipleChoiceField(
                    queryset=tags,
                    widget=forms.CheckboxSelectMultiple(),
                    required=False,
                    label=tag_type.name,
                )
            else:
                # Выбрать только один тег
                self.fields[f'tags_{tag_type.name}'] = forms.ModelChoiceField(
                    queryset=tags,
                    widget=forms.Select(),
                    required=False,
                    label=tag_type.name,
                )

class RecipeEditForm(RecipeCreateForm):
    def __init__(self, *args, **kwargs):
        super(RecipeEditForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            for tag_type in TagType.objects.all():
                tags = instance.tags.filter(tag_type=tag_type)
                if tag_type.multiple_choice:
                    self.initial[f'tags_{tag_type.name}'] = tags.values_list('pk', flat=True)
                else:
                    self.initial[f'tags_{tag_type.name}'] = tags.first().pk if tags.exists() else None

class ProfileUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = False
        self.fields['username'].required = True

    class Meta:
        model = User
        fields = ['first_name', 'email', 'username']

class SearchForm(forms.Form):
    query = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Поиск по названию'}))