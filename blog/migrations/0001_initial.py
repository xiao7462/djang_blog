# Generated by Django 2.2.3 on 2019-12-13 15:36

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mdeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255, verbose_name='公告内容')),
                ('is_publish', models.BooleanField(default=False, verbose_name='是否发布')),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '公告',
                'verbose_name_plural': '公告',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='分类目录名称')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类',
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='站点名称')),
                ('url', models.URLField(max_length=225, verbose_name='站点链接')),
                ('contact_type', models.CharField(choices=[('qq', 'QQ'), ('wechat', '微信'), ('phone', '电话'), ('email', '邮箱')], max_length=255, verbose_name='联系方式')),
                ('contact', models.CharField(max_length=100, verbose_name='联系号码')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否展示')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '友情链接',
                'verbose_name_plural': '友情链接',
            },
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100, unique=True, verbose_name='key值')),
                ('value', models.CharField(max_length=255, verbose_name='value值')),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '系统字典',
                'verbose_name_plural': '系统字典',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='标签')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='标题')),
                ('description', mdeditor.fields.MDTextField(verbose_name='简述')),
                ('content', mdeditor.fields.MDTextField(verbose_name='正文')),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('modified_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='阅读数')),
                ('is_top', models.BooleanField(default=False, verbose_name='顶置文章')),
                ('is_show', models.BooleanField(default=True, verbose_name='发布状态')),
                ('post_type', models.CharField(choices=[('article', '博客文章'), ('about', '关于页面'), ('project', '我的项目')], default='article', max_length=20, verbose_name='类型')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.Category', verbose_name='分类')),
                ('tags', models.ManyToManyField(blank=True, to='blog.Tag', verbose_name='标签')),
            ],
            options={
                'verbose_name': '博客文章',
                'verbose_name_plural': '博客文章',
                'ordering': ['-is_top', '-created_time'],
            },
        ),
    ]
