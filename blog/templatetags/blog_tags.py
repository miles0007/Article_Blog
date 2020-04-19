from django import template
from blog.models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.simple_tag
def total_post():
	return Post.published.count()

@register.inclusion_tag('blog/latest_post.html')
def show_latest_posts(count=5):
	latest_posts = Post.published.order_by('-publish')[:count]
	return {'latest_posts':latest_posts}

@register.simple_tag
def show_most_commented(count=5):
	return Post.published.annotate(total_comment=Count('comment')).order_by('-total_comment')[:count]

@register.filter(name='markdown')
def markdown_format(text):
	return mark_safe(markdown.markdown(text))