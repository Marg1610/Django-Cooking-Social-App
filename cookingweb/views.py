from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Recipe, Tag, TagType, Rating
from .forms import RecipeCreateForm, CustomUserCreationForm, ProfileUpdateForm, RecipeEditForm, SearchForm

def index(request):
    sort = request.GET.get('sort')
    if sort == 'latest':
        recipes = Recipe.objects.order_by('-publication_date')
    elif sort == 'popular':
        recipes = sorted(Recipe.objects.all(), key=lambda x: x.get_rating(), reverse=True)
    else:
        recipes = sorted(Recipe.objects.all(), key=lambda x: x.get_rating(), reverse=True)
    
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {'recipes': page_obj, 'sort': sort})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Имя пользователя уже существует. Пожалуйста, выберите другое имя.')
            else:
                form.save()
                messages.success(request, 'Вы успешно зарегистрировались!')
                return redirect('login')
        else:
            messages.error(request, 'Ошибка при регистрации. Пожалуйста, проверьте введенные данные.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def favorite_recipes(request):
    recipes = Recipe.objects.filter(favorited_by=request.user)
    return render(request, 'favorite_recipes.html', {'favorite_recipes': recipes})

def profile_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_recipes = Recipe.objects.filter(author=user)
    favorite_recipes = Recipe.objects.filter(favorited_by=request.user)

    context = {
        'user': user,
        'user_recipes': user_recipes,
        'favorite_recipes': favorite_recipes,
    }
    return render(request, 'profile_view.html', context)

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile_view', user_id=request.user.id)
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'profile_update.html', {'form': form})

@login_required
def recipe_create(request):
    if request.method == 'POST':
        form = RecipeCreateForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            for tag_type in TagType.objects.all():
                if tag_type.multiple_choice:
                    tags = request.POST.getlist(f'tags_{tag_type.name}')
                else:
                    tags = request.POST.get(f'tags_{tag_type.name}')

                if tags:
                    recipe.tags.add(*tags)

            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeCreateForm()

    if 'image' in request.FILES:
        form.instance.image = request.FILES['image']

    return render(request, 'recipe_create.html', {'form': form})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    is_favorited = False
    if request.user.is_authenticated:
        if request.user in recipe.favorited_by.all():
            is_favorited = True

        user_rating = recipe.rating_set.filter(user=request.user).first()
        if user_rating:
            user_rating = user_rating.value
        else:
            user_rating = None
    else:
        user_rating = None

    if request.method == 'POST':
        if 'favorite_btn' in request.POST and request.user.is_authenticated:
            if is_favorited:
                recipe.favorited_by.remove(request.user)
                is_favorited = False
            else:
                recipe.favorited_by.add(request.user)
                is_favorited = True
    return render(request, 'recipe_detail.html', {'recipe': recipe, 'is_favorited': is_favorited, 'user_rating': user_rating})


@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        form = RecipeEditForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            recipe.tags.clear()

            for tag_type in TagType.objects.all():
                if tag_type.multiple_choice:
                    tags = request.POST.getlist(f'tags_{tag_type.name}')
                else:
                    tags = request.POST.get(f'tags_{tag_type.name}')

                if tags:
                    tag_objects = Tag.objects.filter(pk__in=tags, tag_type=tag_type)
                    recipe.tags.add(*tag_objects)

            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeEditForm(instance=recipe)

    return render(request, 'recipe_update.html', {'form': form})

@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)
    if request.method == 'POST':
        recipe.delete()
        return redirect('index')
    return render(request, 'recipe_delete.html', {'recipe': recipe})

def search(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            recipes = Recipe.objects.filter(title__icontains=query)
            return render(request, 'search_results.html', {'recipes': recipes, 'query': query})
    else:
        form = SearchForm()
    return render(request, 'index.html', {'form': form})

@login_required
def like_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    user = request.user

    rating = recipe.rating_set.filter(user=user).first()

    if rating:
        if rating.value == Rating.LIKE:
            rating.delete()
        else:
            rating.value = Rating.LIKE
            rating.save()
    else:
        rating = Rating(value=Rating.LIKE, recipe=recipe, user=user)
        rating.save()

    return redirect('recipe_detail', pk=recipe.pk)

@login_required
def dislike_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    user = request.user

    rating = recipe.rating_set.filter(user=user).first()

    if rating:
        if rating.value == Rating.DISLIKE:
            rating.delete()
        else:
            rating.value = Rating.DISLIKE
            rating.save()
    else:
        rating = Rating(value=Rating.DISLIKE, recipe=recipe, user=user)
        rating.save()

    return redirect('recipe_detail', pk=recipe.pk)
