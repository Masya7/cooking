from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Категория')
    description = models.TextField(blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Ингредиент')
    unit = models.CharField(max_length=50, verbose_name='Единица измерения', blank=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название рецепта')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='recipes', verbose_name='Категория')
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', verbose_name='Ингредиенты')
    main_ingredient = models.ForeignKey(Ingredient, on_delete=models.SET_NULL, null=True, blank=True, related_name='main_recipes', verbose_name='Главный ингредиент')
    COOKING_METHOD_CHOICES = [
        ('boil', 'Варка'),
        ('fry', 'Жарка'),
        ('bake', 'Запекание'),
        ('stew', 'Тушение'),
        ('grill', 'Гриль'),
        ('steam', 'Пар'),
        ('raw', 'Без термообработки'),
        ('other', 'Другое'),
    ]
    cooking_method = models.CharField(max_length=20, choices=COOKING_METHOD_CHOICES, default='other', verbose_name='Метод приготовления')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes', verbose_name='Автор')
    image = models.ImageField(upload_to='recipes/', blank=True, null=True, verbose_name='Изображение')
    cooking_time = models.PositiveIntegerField(verbose_name='Время приготовления (мин)')
    calories = models.PositiveIntegerField(verbose_name='Калории', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title
    
    def average_rating(self):
        """Возвращает средний рейтинг рецепта"""
        avg = self.ratings.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0
    
    def rating_count(self):
        """Возвращает количество оценок"""
        return self.ratings.count()

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.CharField(max_length=100, verbose_name='Количество')

    def __str__(self):
        return f"{self.ingredient.name} для {self.recipe.title}"

class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings', verbose_name='Рецепт')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings', verbose_name='Пользователь')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оценка'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата оценки')

    class Meta:
        unique_together = ('recipe', 'user')  # Один пользователь может оценить рецепт только один раз

    def __str__(self):
        return f"Оценка {self.rating} для {self.recipe.title} от {self.user.username}"

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments', verbose_name='Рецепт')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')
    author_name = models.CharField(max_length=100, verbose_name='Имя автора', help_text='Отображаемое имя', default='Аноним')
    text = models.TextField(verbose_name='Комментарий')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оценка',
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Комментарий от {self.author_name} к {self.recipe.title}"
