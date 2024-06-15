from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('recipe/create/', views.recipe_create, name='recipe_create'),
    path('<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('recipe/<int:pk>/update/', views.recipe_edit, name='recipe_update'),
    path('profile/<int:user_id>/', views.profile_view, name='profile_view'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('recipe/<int:pk>/delete/', views.recipe_delete, name='recipe_delete'),
    path('search/', views.search, name='search'),
    path('recipe/<int:pk>/like/', views.like_recipe, name='like_recipe'),
    path('recipe/<int:pk>/dislike/', views.dislike_recipe, name='dislike_recipe'),
    path('favorites/', views.favorite_recipes, name='favorites'),

]
