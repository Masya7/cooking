import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Recipe, Rating, Comment

# Список имен для авторов отзывов
REVIEWER_NAMES = [
    'Анна Кулинарова', 'Михаил Поваров', 'Елена Вкусняшкина', 'Дмитрий Шефов',
    'Ольга Рецептова', 'Александр Готовкин', 'Мария Блюдова', 'Николай Едов',
    'Светлана Кухаркина', 'Владимир Специйский', 'Татьяна Сладкова', 'Сергей Мясной',
    'Ирина Овощная', 'Павел Соусов', 'Екатерина Десертова', 'Игорь Гриллер'
]

# Шаблоны отзывов по рейтингам
REVIEW_TEMPLATES = {
    5: [
        "Великолепный рецепт! Получилось невероятно вкусно, вся семья в восторге!",
        "Потрясающе! Готовила уже несколько раз - всегда идеальный результат.",
        "Шедевр! Этот рецепт стал моим любимым, готовлю постоянно.",
        "Восхитительно! Даже мой придирчивый муж попросил добавки.",
        "Фантастический рецепт! Гости до сих пор просят поделиться секретом."
    ],
    4: [
        "Очень вкусно! Небольшие коррективы по специям и будет идеально.",
        "Отличный рецепт! Легко готовить, результат превосходный.",
        "Хороший рецепт! Детям понравилось, буду готовить ещё.",
        "Классно получилось! Добавила немного своих ингредиентов.",
        "Замечательное блюдо! Время готовки точное, всё понятно."
    ],
    3: [
        "Неплохо, но можно улучшить. Добавила больше специй.",
        "Средненько. Вкусно, но ничего особенного.",
        "Нормальный рецепт. Для разнообразия подойдёт.",
        "Готовила по рецепту - получилось, но ожидала большего.",
        "Обычное блюдо. Семье понравилось, но не в восторге."
    ],
    2: [
        "Не очень. Что-то пошло не так, получилось пресно.",
        "Разочарована. Может, что-то не так делала, но вкус слабый.",
        "Слишком простой рецепт. Ожидала более яркого вкуса.",
        "Не впечатлило. Видимо, не мой тип блюд.",
        "Пробовала готовить - результат посредственный."
    ],
    1: [
        "Не понравилось совсем. Зря потратила время и продукты.",
        "Ужасно! Семья даже есть не стала.",
        "Полный провал. Что-то не то с рецептом.",
        "Катастрофа! Пришлось заказывать пиццу на ужин.",
        "Безвкусно и неаппетитно. Больше готовить не буду."
    ]
}

class Command(BaseCommand):
    help = 'Добавляет рейтинги и отзывы к существующим рецептам'

    def handle(self, *args, **kwargs):
        # Очищаем существующие рейтинги и комментарии
        Rating.objects.all().delete()
        Comment.objects.all().delete()
        
        # Получаем или создаём тестового пользователя
        test_user, _ = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'test@example.com'}
        )
        
        recipes = Recipe.objects.all()
        total_reviews = 0
        total_ratings = 0
        
        for recipe in recipes:
            # Генерируем от 1 до 7 отзывов для каждого рецепта
            num_reviews = random.randint(1, 7)
            
            for i in range(num_reviews):
                # Случайный рейтинг от 1 до 5 с уклоном в сторону высоких оценок
                rating_value = random.choices([1, 2, 3, 4, 5], weights=[5, 10, 20, 35, 30])[0]
                
                # Создаём рейтинг
                try:
                    # Создаём уникальных пользователей для каждого отзыва
                    reviewer_username = f"reviewer_{recipe.id}_{i}"
                    reviewer, _ = User.objects.get_or_create(
                        username=reviewer_username,
                        defaults={'email': f'{reviewer_username}@example.com'}
                    )
                    
                    rating = Rating.objects.create(
                        recipe=recipe,
                        user=reviewer,
                        rating=rating_value
                    )
                    total_ratings += 1
                    
                    # Создаём комментарий с тем же рейтингом
                    review_text = random.choice(REVIEW_TEMPLATES[rating_value])
                    author_name = random.choice(REVIEWER_NAMES)
                    
                    comment = Comment.objects.create(
                        recipe=recipe,
                        author=reviewer,
                        author_name=author_name,
                        text=review_text,
                        rating=rating_value
                    )
                    total_reviews += 1
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'Ошибка при создании отзыва для рецепта {recipe.title}: {e}')
                    )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Успешно добавлено {total_ratings} рейтингов и {total_reviews} отзывов!'
            )
        )
        
        # Статистика по рейтингам
        for recipe in recipes[:5]:  # Показываем статистику для первых 5 рецептов
            avg_rating = recipe.average_rating()
            rating_count = recipe.rating_count()
            self.stdout.write(
                f'{recipe.title}: {avg_rating}/5 ⭐ ({rating_count} оценок)'
            ) 