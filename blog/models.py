from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from mdeditor.fields import MDTextField
import time
from django.utils import timezone
from django.db.models import Q, Count


class Page(object):
    """
    数据分页管理工具
    """
    def __init__(self, count, current_page=1, num=40):
        self.count = count  # 总数
        self.current_page = current_page  # 当前页数
        self.num = num  # 每页数量
        self.pages = self.count // self.num + (1 if self.count % self.num else 0)

        if self.pages == 0 or self.current_page < 1 or self.current_page > self.pages:
            self.start = 0
            self.end = 0
            self.index = 1
        else:
            self.start = (self.current_page - 1) * self.num
            self.end = self.num + self.start
            self.index = self.current_page

        self.prev = self.index - 1 if self.index > 1 else self.index
        self.next = self.index + 1 if self.index < self.pages else self.index


# 上传文件目录
def upload_path(instance, old_filename):
    """封面上传"""
    extension = old_filename.split('.', 1)[1].lower()
    file_name = old_filename.split('.', 1)[0].lower()
    timestamp = int(time.time())

    file_path = 'cover/{file_name}-{timestamp}.{extension}'.format(
        timestamp=timestamp,
        file_name=file_name,
        extension=extension)
    return file_path


class CategoryManager(models.Manager):
    """
    分类管理
    """
    def get_all_categories(self, post_type='article'):
        return self.get_queryset().filter(article__is_show=True, article__post_type=post_type).all().distinct()


class Category(models.Model):
    """
    文章分类
    """
    name = models.CharField(max_length=50, unique=True, verbose_name='分类目录名称')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'

    objects = CategoryManager()


class TagManager(models.Manager):
    """
    标签管理
    """
    def get_tags_count(self, post_type='article'):
        tags = self.get_queryset().filter(article__is_show=True, article__post_type=post_type).\
            annotate(num_articles=Count('article')).filter(num_articles__gt=0).order_by('-num_articles')
        return tags

    def get_tags_cloud(self, post_type='article', num=None):
        returned_tags = []
        tags = self.get_queryset().filter(article__is_show=True, article__post_type=post_type).\
            annotate(num_articles=Count('article')).filter(num_articles__gt=0).order_by('-num_articles')
        if num:
            tags = tags[:int(num)]
        for tag in tags:
            returned_tags.append({'label': f'{tag.name}({tag.num_articles})', 'url': reverse('blog:tag_index', kwargs={'tag': tag.name}),
                                  'target': '_blank'})
        return returned_tags


class Tag(models.Model):
    """
    文章标签
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='标签')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'

    objects = TagManager()


class ArticleManager(models.Manager):
    """
    文章管理
    """

    # 取得所有文章
    def get_all_articles(self, post_type='article', search_key=None):
        if search_key:
            query_set = self.get_queryset().filter(is_show=True, post_type=post_type). \
                filter(Q(title__icontains=search_key) |
                       Q(description__icontains=search_key) |
                       Q(category__name__icontains=search_key) |
                       Q(tag__name__icontains=search_key))
        else:
            query_set = self.get_queryset().filter(is_show=True, post_type=post_type)
        return query_set

    # 取得所有文章, 分页显示
    def get_paged_articles(self, current_page=1, num=10, post_type='article', search_key=None):
        if search_key:
            query_set = self.get_queryset().filter(is_show=True, post_type=post_type). \
                filter(Q(title__icontains=search_key) |
                       Q(description__icontains=search_key) |
                       Q(category__name__icontains=search_key) |
                       Q(tag__name__icontains=search_key))
        else:
            query_set = self.get_queryset().filter(is_show=True, post_type=post_type)
        count = query_set.count()
        page = Page(count, current_page, num)
        query = query_set.order_by('-created_time', '-id')[page.start:page.end]
        return query, page

    # 根据目录ID取出所属文章/分页显示
    def get_paged_articles_by_category(self, category, num=10, current_page=1, post_type='article', search_key=None):
        if search_key:
            query_set = self.get_queryset().filter(is_show=True, post_type=post_type,
                                                   category__name__icontains=category) \
                .filter(
                Q(title__icontains=search_key) |
                Q(description__icontains=search_key) |
                Q(category__name__icontains=search_key) |
                Q(tag__name__icontains=search_key)
            )
        else:
            query_set = self.get_queryset().filter(is_show=True, post_type=post_type, category__name__icontains=category)
        count = query_set.count()
        page = Page(count, current_page, num)
        query = query_set.order_by('-created_time', '-id')[page.start:page.end]
        return query, page

    # 根据标签ID取出文章/分页显示
    def get_paged_articles_by_tag(self, tag, num=10, current_page=1, post_type='article', search_key=None):
        if search_key:
            query_set = self.get_queryset().filter(is_show=True, post_type=post_type,
                                                   tags__name__icontains=tag). \
                filter(
                Q(title__icontains=search_key) |
                Q(description__icontains=search_key) |
                Q(category__name__icontains=search_key) |
                Q(tag__name__icontains=search_key)
            )
        else:
            query_set = self.get_queryset().filter(is_show=True, post_type=post_type, tags__name__icontains=tag)
        count = query_set.count()
        page = Page(count, current_page, num)
        query = query_set.order_by('-created_time', '-id')[page.start:page.end]
        return query, page


class Article(models.Model):
    """
    博客正文内容
    """
    # 文章标题、目录与正文
    title = models.CharField(max_length=255, verbose_name='标题')
    # cover = models.ImageField(upload_to=upload_path, verbose_name="封面")
    description = MDTextField(verbose_name='简述')
    content = MDTextField(verbose_name='正文')

    category = models.ForeignKey(Category, verbose_name='分类', null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')

    # 文章创建时间和最近更新时间
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    # 文章访问量
    views = models.PositiveIntegerField(default=0, verbose_name='阅读数')

    # 文章是否顶置，默认不顶置
    is_top = models.BooleanField(default=False, verbose_name='顶置文章')
    # 文章发布状态，默认是创建成功就发布
    is_show = models.BooleanField(default=True, verbose_name='发布状态')

    # 文章类型：注意 about 和 project 只能创建一个
    post_type = models.CharField(max_length=20,
                                 choices=(('article', '博客文章'),
                                          ('about', '关于页面'),
                                          ('project', '我的项目'),
                                          ),
                                 default='article',
                                 verbose_name='类型'
                                 )

    def __str__(self):
        return self.title

    # 自定义 get_absolute_url 方法
    def get_absolute_url(self):
        return reverse('blog:article', kwargs={'pk': self.pk})

    # 自定义 get_absolute_url 方法
    def get_project_absolute_url(self):
        return reverse('blog:project', kwargs={'pk': self.pk})

    # 自定义 increase_views 方法：用于统计访问量
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    class Meta:
        # 获取 Post 列表时，按照顶置、创建时间排序
        ordering = ['-is_top', '-created_time']
        verbose_name = '博客文章'
        verbose_name_plural = '博客文章'

    objects = ArticleManager()


class LinkManager(models.Manager):
    """
    友情链接管理
    """
    pass


class Link(models.Model):
    """
    友情链接
    """
    name = models.CharField(max_length=100, verbose_name='站点名称')
    url = models.URLField(max_length=225, verbose_name='站点链接')
    contact_type = models.CharField(max_length=255, choices=(('qq', 'QQ'),
                                                             ('wechat', '微信'),
                                                             ('phone', '电话'),
                                                             ('email', '邮箱'),),
                                    verbose_name="联系方式")
    contact = models.CharField(max_length=100, verbose_name="联系号码")

    is_show = models.BooleanField(default=True, verbose_name='是否展示')

    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = '友情链接'

    objects = LinkManager()


class AnnouncementManager(models.Manager):
    """公告管理"""
    pass


class Announcement(models.Model):
    """
    公告
    """
    content = models.CharField(max_length=255, verbose_name="公告内容")
    is_publish = models.BooleanField(default=False, verbose_name="是否发布")
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = '公告'

    objects = AnnouncementManager()


class SettingManager(models.Manager):
    """系统字典管理"""
    def get_value_by_key(self, key):
        return self.get_queryset().filter(key=key).values('value')


class Setting(models.Model):
    """
    系统字典
    """
    key = models.CharField(max_length=100, unique=True, verbose_name="key值")
    value = models.CharField(max_length=255, verbose_name="value值")
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = '系统字典'
        verbose_name_plural = '系统字典'

    objects = SettingManager()
