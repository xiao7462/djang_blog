from django.contrib import admin
from blog.models import Category, Article, Tag, Link, Announcement, Setting


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_time')
    search_fields = ('name',)
    list_filter = ('created_time',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_time')
    search_fields = ('name',)
    list_filter = ('created_time',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_time', 'modified_time', 'views', 'is_top', 'is_show', 'post_type')
    search_fields = ('title',)
    list_filter = ('created_time', 'modified_time', 'is_top', 'is_show', 'post_type')


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'contact_type', 'contact', 'is_show')
    search_fields = ('title', 'category')
    list_filter = ('created_time', 'contact_type', 'is_show')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('content', 'is_publish')
    search_fields = ('content',)
    list_filter = ('created_time', 'is_publish',)


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')
    search_fields = ('key', 'value')
    list_filter = ('created_time',)
