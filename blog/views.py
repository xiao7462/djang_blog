from django.shortcuts import render, get_object_or_404
from django.views import View
from blog.models import Article, Tag, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db.models.aggregates import Count
import json, re
from django.http import HttpResponse
from django_hexo_blog.views import page_not_found
from blog.utils import MD
from django.conf import settings


def index(request):
    # 博客首页
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1
    blog_articles, page = Article.objects.get_paged_articles(current_page=current_page)
    return render(request, 'blog/index.html', context={
        'blog_articles': blog_articles,
        'page': page,
    })


def tag_index(request, tag):
    # 拥有指定标签的文章
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1
    blog_articles, page = Article.objects.get_paged_articles_by_tag(tag=tag, current_page=current_page)
    return render(request, 'blog/index.html', context={
        'blog_articles': blog_articles,
        'page': page,
    })


def category_index(request, category):
    # 指定分类下的文章
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1
    blog_articles, page = Article.objects.get_paged_articles_by_category(category=category, current_page=current_page)
    return render(request, 'blog/index.html', context={
        'blog_articles': blog_articles,
        'page': page,
    })


def detail(request, pk):
    # 文章详情
    article = get_object_or_404(Article, pk=pk)
    # 调用 increase_views 方法，统计访问量
    article.increase_views()
    return render(request, 'blog/detail.html', context={'article': article})


# 标签页面
def tags(request):
    return render(request, 'blog/tags.html')


# 标签页面
def tags_cloud(request):
    num = request.GET.get('num', None)
    all_tags = Tag.objects.get_tags_cloud(num=num)
    return HttpResponse(json.dumps(all_tags, ensure_ascii=False),content_type="application/json,charset=utf-8")


# 归档页面
def categories(request):
    all_categories = Category.objects.get_all_categories()
    articles = Article.objects.get_all_articles()
    return render(request, 'blog/categories.html', context={'articles': articles, 'categories': all_categories})


# 归档页面
def archives(request):
    years = Article.objects.filter(is_show=True, post_type='article').dates('created_time', 'year', order='DESC')
    post_list = Article.objects.filter(is_show=True, post_type='article').order_by('-created_time')
    return render(request, 'blog/archives.html', context={'years':years, 'post_list':post_list})


# 我的项目
def project(request):
    projects = Article.objects.get_all_articles(post_type='project')
    return render(request, 'blog/project.html', context={'projects': projects})


def project_detail(request, pk):
    # 文章详情
    pro = get_object_or_404(Article, pk=pk)
    # 调用 increase_views 方法，统计访问量
    pro.increase_views()
    return render(request, 'blog/project_detail.html', context={'project': pro})


# 关于页面
def about(request):
    article = Article.objects.filter(post_type='about').first()
    if article:
        md = MD()
        article.content = md.convert(article.content)
        article.toc = md.toc
        article.increase_views()  # 调用 increase_views 方法，统计访问量
        return render(request, 'blog/about.html', context={'article': article})
    else:
        return page_not_found(request)


# 搜索请求
def search(request, ):
    # 搜索内容
    if request.method == 'GET':
        q = request.GET.get('q')
        article_list = Article.objects.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(description__icontains=q),
                                              is_show=True, post_type='article')

        data = {'posts':[]}
        for article in article_list:
            data['posts'].append({
                "title":article.title,
                "permalink":article.get_absolute_url(),
                "text":article.content
            },)
        return HttpResponse(json.dumps(data, ensure_ascii=False),content_type="application/json,charset=utf-8")
    else:
        pass