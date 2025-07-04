from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author_name', 'text', 'rating']
        widgets = {
            'author_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя',
                'required': True
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Поделитесь своим мнением о рецепте...',
                'rows': 4,
                'required': True
            }),
            'rating': forms.Select(
                choices=[(i, f'{i} звёзд{"а" if i in [2, 3, 4] else ("ы" if i == 1 else "")}') for i in range(1, 6)],
                attrs={
                    'class': 'form-select',
                    'required': True
                }
            )
        }
        labels = {
            'author_name': 'Ваше имя',
            'text': 'Отзыв',
            'rating': 'Оценка'
        } 