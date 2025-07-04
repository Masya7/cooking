import os
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Category, Ingredient, Recipe, RecipeIngredient

# Список ингредиентов для генерации случайных рецептов
ingredients_pool = [
    'Курица', 'Свинина', 'Говядина', 'Лосось', 'Тунец', 'Креветки', 'Рис', 'Картофель',
    'Морковь', 'Брокколи', 'Помидор', 'Огурец', 'Капуста', 'Перец', 'Лук', 'Чеснок',
    'Имбирь', 'Соевый соус', 'Оливковое масло', 'Сливочное масло', 'Соль', 'Перец черный',
    'Базилик', 'Орегано', 'Петрушка', 'Кинза', 'Лайм', 'Лимон', 'Мука', 'Сахар', 'Мед', 'Молоко', 'Сливки',
    'Сыр моцарелла', 'Сыр чеддер', 'Яйца', 'Грибы', 'Тофу', 'Баклажан', 'Цуккини', 'Кокосовое молоко', 'Авокадо',
    'Фасоль', 'Горох', 'Кукуруза', 'Чечевица', 'Спагетти', 'Лапша', 'Рамен', 'Хлеб'
]

methods = ['boil', 'bake', 'fry', 'steam', 'grill']
categories_list = ['Супы', 'Горячее', 'Закуски', 'Салаты']

# Шаблоны названий для азиатских блюд
asian_dish_templates = [
    '{main} по-китайски', '{main} в соевом соусе', '{main} по-тайски', '{main} терияки',
    '{main} с имбирем', '{main} по-корейски', '{main} в кисло-сладком соусе', '{main} по-японски',
    'Острый {main}', '{main} с овощами по-азиатски', '{main} в воке', '{main} с рисом',
    '{main} по-вьетнамски', '{main} в кокосовом молоке', '{main} карри'
]

# Шаблоны названий для европейских блюд
european_dish_templates = [
    '{main} по-французски', '{main} по-итальянски', '{main} запеченный', '{main} тушеный',
    '{main} в сливочном соусе', '{main} гриль', '{main} по-немецки', '{main} с травами',
    '{main} по-средиземноморски', '{main} в вине', '{main} с чесноком', '{main} по-испански',
    '{main} фламбе', '{main} конфи', '{main} с прованскими травами'
]

ASIA_PHOTOS = [f"photo_{i+1}_2025-07-01_22-40-55.jpg" for i in range(25)]
EUROPE_PHOTOS = [f"photo_{i+1}_2025-07-01_22-37-32.jpg" for i in range(25)]

# Генерация рецептов
def generate_recipe(photo, is_asian=True):
    ingredients = random.sample(ingredients_pool, 5)
    main_ingredient = ingredients[0]
    
    # Выбираем шаблон названия в зависимости от региона
    if is_asian:
        title_template = random.choice(asian_dish_templates)
    else:
        title_template = random.choice(european_dish_templates)
    
    title = title_template.format(main=main_ingredient)
    cooking_method = random.choice(methods)
    
    # Создаём более детальные пошаговые инструкции в зависимости от способа приготовления
    if cooking_method == 'fry':
        steps = [
            f'Подготовьте {ingredients[0].lower()}: вымойте, обсушите и нарежьте порционными кусочками.',
            f'Разогрейте сковороду с растительным маслом на среднем огне.',
            f'Обжарьте {ingredients[1].lower()} до золотистого цвета, примерно 3-4 минуты.',
            f'Добавьте {ingredients[2].lower()} и жарьте ещё 2-3 минуты, помешивая.',
            f'Приправьте {ingredients[3].lower()}, {ingredients[4].lower()}, солью и перцем по вкусу.',
            'Убавьте огонь, накройте крышкой и готовьте ещё 5-7 минут.',
            'Подавайте горячим, украсив свежей зеленью и дольками лимона.'
        ]
    elif cooking_method == 'bake':
        steps = [
            f'Разогрейте духовку до 180°C. Подготовьте форму для запекания.',
            f'Нарежьте {ingredients[0].lower()} и {ingredients[1].lower()} крупными кусками.',
            f'Сложите ингредиенты в форму, добавьте {ingredients[2].lower()}.',
            f'Смешайте {ingredients[3].lower()} с {ingredients[4].lower()}, солью и специями.',
            'Полейте смесью подготовленные ингредиенты, перемешайте.',
            'Накройте фольгой и запекайте 45-60 минут до готовности.',
            'За 10 минут до готовности снимите фольгу для образования золотистой корочки.'
        ]
    elif cooking_method == 'boil':
        steps = [
            f'В большой кастрюле доведите до кипения 2 литра подсоленной воды.',
            f'Подготовьте {ingredients[0].lower()}: очистите и нарежьте кубиками.',
            f'Опустите {ingredients[1].lower()} в кипящую воду, варите 10 минут.',
            f'Добавьте {ingredients[2].lower()} и {ingredients[3].lower()}, варите ещё 15 минут.',
            f'За 5 минут до готовности добавьте {ingredients[4].lower()} и специи.',
            'Попробуйте на соль и при необходимости досолите.',
            'Подавайте горячим с хлебом и сметаной.'
        ]
    elif cooking_method == 'steam':
        steps = [
            'Подготовьте пароварку или мантоварку, налейте воду в нижний ярус.',
            f'Нарежьте {ingredients[0].lower()} тонкими пластинками.',
            f'Смешайте {ingredients[1].lower()} с {ingredients[2].lower()} и специями.',
            f'Выложите {ingredients[3].lower()} на дно корзины пароварки.',
            'Разложите подготовленные ингредиенты в один слой.',
            f'Готовьте на пару 20-25 минут, посыпьте {ingredients[4].lower()}.',
            'Подавайте сразу после приготовления с соусом.'
        ]
    else:  # grill и другие
        steps = [
            f'Подготовьте {ingredients[0].lower()}: замаринуйте в специях на 30 минут.',
            'Разогрейте гриль или сковороду-гриль до высокой температуры.',
            f'Нарежьте {ingredients[1].lower()} и {ingredients[2].lower()} крупными кусками.',
            f'Обжарьте основной ингредиент по 4-5 минут с каждой стороны.',
            f'Добавьте {ingredients[3].lower()} и {ingredients[4].lower()}.',
            'Готовьте ещё 3-4 минуты до образования аппетитных полосок.',
            'Дайте отдохнуть 2-3 минуты перед подачей.'
        ]
    
    return {
        'title': title,
        'description': f'{title} – изысканное блюдо с богатым вкусом и ароматом. Идеально подходит для праздничного стола.',
        'category': random.choice(categories_list),
        'main_ingredient': main_ingredient,
        'cooking_method': cooking_method,
        'cooking_time': random.randint(15, 90),
        'calories': random.randint(150, 450),
        'steps': steps,
        'ingredients': [(ing, f'{random.randint(50, 250)} г') for ing in ingredients],
        'photo': photo
    }

ASIAN_RECIPES = [generate_recipe(ASIA_PHOTOS[i], is_asian=True) for i in range(25)]
EUROPEAN_RECIPES = [generate_recipe(EUROPE_PHOTOS[i], is_asian=False) for i in range(25)]

class Command(BaseCommand):
    help = 'Populate the database with 50 unique recipes with proper images'

    def handle(self, *args, **kwargs):
        RecipeIngredient.objects.all().delete()
        Recipe.objects.all().delete()
        Ingredient.objects.all().delete()
        Category.objects.all().delete()

        user, _ = User.objects.get_or_create(username='testuser', defaults={'password': 'testpass'})

        categories = {name: Category.objects.create(name=name) for name in categories_list}

        ingredients_dict = {}
        for ing in ingredients_pool:
            ingredients_dict[ing], _ = Ingredient.objects.get_or_create(name=ing, defaults={'unit': 'г'})

        for recipe_list, region in [(ASIAN_RECIPES, 'asia'), (EUROPEAN_RECIPES, 'europe')]:
            for rec in recipe_list:
                photo_path = f'{region}/{rec["photo"]}'
            recipe = Recipe.objects.create(
                title=rec['title'],
                description=rec['description'] + '\n' + '\n'.join(f'{n+1}. {step}' for n, step in enumerate(rec['steps'])),
                category=categories[rec['category']],
                main_ingredient=ingredients_dict[rec['main_ingredient']],
                cooking_method=rec['cooking_method'],
                author=user,
                cooking_time=rec['cooking_time'],
                calories=rec['calories'],
                    image=photo_path
            )
            for name, amount in rec['ingredients']:
                RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredients_dict[name], amount=amount)

        self.stdout.write(self.style.SUCCESS('50 уникальных рецептов успешно добавлены!'))
