from django.contrib import admin
from .models import Category, News, NewsComment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'status', 'created_at', 'views')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views', 'created_at', 'updated_at')

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'content', 'short_description', 'category', 'author', 'image')
        }),
        ('Статус и даты', {
            'fields': ('status', 'published_at', 'created_at', 'updated_at')
        }),
        ('Дополнительно', {
            'fields': ('tags', 'views', 'meta_title', 'meta_description')
        }),
    )


@admin.register(NewsComment)
class NewsCommentAdmin(admin.ModelAdmin):
    list_display = ('news', 'user', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('content', 'user__username', 'news__title')