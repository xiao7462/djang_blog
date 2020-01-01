# -*- coding: utf-8 -*-

from django.urls import path
from . import views as blog_views

app_name = 'blog'

urlpatterns = [
    path('', blog_views.index, name='index'),
    path('tag/<tag>/', blog_views.tag_index, name='tag_index'),
    path('category/<category>/', blog_views.category_index, name='category_index'),

    path('categories/', blog_views.categories, name='categories'),
    path('tags/', blog_views.tags, name='tags'),
    path('tags_cloud/', blog_views.tags_cloud, name='tags_cloud'),
    path('archives/', blog_views.archives, name='archives'),

    path('projects/', blog_views.project, name='projects'),

    path('project/<int:pk>/', blog_views.project_detail, name='project'),
    path('article/<int:pk>/', blog_views.detail, name='article'),

    path('about/', blog_views.about, name='about'),

    path('content.json/', blog_views.search, name='search'),



]
