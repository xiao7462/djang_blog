import markdown
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension


def MD():
    """转换markdown"""
    return markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
    ])


