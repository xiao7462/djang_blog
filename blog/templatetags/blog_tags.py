# -*- coding: utf-8 -*-

from blog.models import Article, Tag, Link, Setting, Announcement
from django import template
from django.db.models.aggregates import Count
from django_hexo_blog.settings import SITE_CONFIGS
from blog.utils import MD
import random
register = template.Library()


@register.filter
def make_markdown(content):
    return MD().convert(content)


@register.filter
def make_toc(content):
    md = MD()
    md.convert(content)
    return md.toc


# 获取最新5篇文章
@register.simple_tag
def get_recent_posts(num=5):
    return Article.objects.filter(is_show=True).order_by('-created_time')[:num]


# 获取文章归档
@register.simple_tag
def get_archives():
    return Article.objects.filter(is_show=True).dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_tags():
    # 使用 Count 方法统计文章数，并保存到 num_posts 属性中
    #style="background-color:#B04518" 别人的
    #style="font-size:14px;color:#999"  自己的
    # 标签云的样式
    color_array =  [
        '0', '1', '2', '3', '4', '5', '6', '7',
        '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'
    ]
    tags_style = []
    for _ in range(20):
        color = '#' + ''.join(random.sample(color_array, 6)) # 高亮
        # num = random.randint(11, 13)
        num = 13
        # tags_style.append("font-size:{}px;color:{}".format(num,color))
        tags_style.append("font-size:{}px;\
            background-color:{} ;\
            padding-left:5px; padding-right:5px; \
            padding:5px 5px 7px 5px;\
            display: inline-block;\
            margin: 3px 3px;\
            border-radius: 10px;\
            color : #faf6f6".format(num,color))
    
    tags = Tag.objects.filter(article__is_show=True).annotate(num_posts=Count('article')).filter(num_posts__gt=0).order_by('-num_posts')#[:10]
    return {'tags_style':tags_style, 'tags':tags}


# 获取友情链接
@register.simple_tag
def get_links():
    return Link.objects.filter(is_show=True)


@register.simple_tag
def get_announcements():
    return Announcement.objects.filter(is_publish=True).order_by('-created_time')


# 站点配置
@register.simple_tag
def get_site_configs():
    exclude_keys = []
    for key, value in SITE_CONFIGS.items():
        site_setting = Setting.objects.filter(key=key).first()
        exclude_keys.append(key)
        if site_setting:
            SITE_CONFIGS[key] = site_setting.value
    site_settings = Setting.objects.exclude(key__in=exclude_keys).all()
    for site_setting in site_settings:
        SITE_CONFIGS[site_setting.key] = site_setting.value
    return SITE_CONFIGS
