from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.home, name='home'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    # В дальнейшем здесь будут маршруты для рецептов
] 