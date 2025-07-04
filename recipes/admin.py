from django.contrib import admin
from .models import Category, Ingredient, Recipe, RecipeIngredient, Comment

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ('title', 'author', 'category', 'cooking_time', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('category', 'author')

admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Comment)
