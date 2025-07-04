from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Recipe, Ingredient, Category, RecipeIngredient, Rating
from .forms import CommentForm

def home(request):
    recipes = Recipe.objects.all().select_related('category', 'main_ingredient').prefetch_related('ingredients', 'ratings')
    categories = Category.objects.all()
    ingredients = Ingredient.objects.all()
    methods = Recipe.COOKING_METHOD_CHOICES

    # Фильтрация
    category_id = request.GET.get('category')
    ingredient_id = request.GET.get('ingredient')
    method = request.GET.get('method')
    search = request.GET.get('search')

    if category_id:
        recipes = recipes.filter(category_id=category_id)
    if ingredient_id:
        recipes = recipes.filter(main_ingredient_id=ingredient_id)
    if method:
        recipes = recipes.filter(cooking_method=method)
    if search:
        recipes = recipes.filter(title__icontains=search)

    context = {
        'recipes': recipes,
        'categories': categories,
        'ingredients': ingredients,
        'methods': methods,
        'selected_category': category_id,
        'selected_ingredient': ingredient_id,
        'selected_method': method,
    }
    return render(request, 'recipes/recipe_list.html', context)

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe.objects.select_related('category', 'main_ingredient', 'author').prefetch_related('ingredients', 'recipeingredient_set'), pk=pk)
    ingredients = recipe.recipeingredient_set.all()
    portions = int(request.GET.get('portions', 1))
    
    # Получаем комментарии с рейтингами
    comments = recipe.comments.all()[:10]  # Показываем первые 10 комментариев
    
    # Обработка формы отзыва
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            # Создаём временного пользователя или используем существующего
            author_username = f"user_{comment.author_name.replace(' ', '_').lower()}"
            user, created = User.objects.get_or_create(
                username=author_username,
                defaults={'email': f'{author_username}@example.com'}
            )
            comment.author = user
            comment.save()
            
            # Создаём соответствующий рейтинг
            Rating.objects.update_or_create(
                recipe=recipe,
                user=user,
                defaults={'rating': comment.rating}
            )
            
            messages.success(request, 'Спасибо за ваш отзыв! Он был успешно добавлен.')
            return redirect('recipe_detail', pk=pk)
    else:
        form = CommentForm()
    
    # Извлекаем инструкции из description
    description_lines = recipe.description.split('\n')
    main_description = description_lines[0] if description_lines else ''
    
    # Находим строки с номерами шагов (начинающиеся с цифры и точки)
    steps = []
    for line in description_lines[1:]:  # Пропускаем первую строку (основное описание)
        line = line.strip()
        if line and (line[0].isdigit() and '. ' in line[:4]):
            # Убираем номер шага из текста
            step_text = line.split('. ', 1)[1] if '. ' in line else line
            steps.append(step_text)
    
    # Пересчёт ингредиентов для указанного количества порций
    if portions > 1:
        for ingredient in ingredients:
            # Извлекаем числовое значение из строки количества
            amount_str = ingredient.amount
            try:
                # Пытаемся найти число в начале строки
                import re
                amount_match = re.search(r'^(\d+(?:\.\d+)?)', amount_str)
                if amount_match:
                    base_amount = float(amount_match.group(1))
                    unit = amount_str.replace(amount_match.group(1), '').strip()
                    new_amount = base_amount * portions
                    ingredient.calculated_amount = f"{int(new_amount) if new_amount.is_integer() else new_amount:.1f} {unit}"
                else:
                    ingredient.calculated_amount = ingredient.amount
            except:
                ingredient.calculated_amount = ingredient.amount
    else:
        for ingredient in ingredients:
            ingredient.calculated_amount = ingredient.amount
    
    context = {
        'recipe': recipe,
        'ingredients': ingredients,
        'portions': portions,
        'main_description': main_description,
        'steps': steps,
        'comments': comments,
        'average_rating': recipe.average_rating(),
        'rating_count': recipe.rating_count(),
        'comment_form': form,
    }
    return render(request, 'recipes/recipe_detail.html', context)

# Create your views here.
