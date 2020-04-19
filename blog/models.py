from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from cloudinary.models import CloudinaryField
# Create your models here.
class PublishedManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(status='published')

class Post(models.Model):
	status_choices = {('draft','Draft'),('published','Published')}
	title = models.CharField(max_length=250)
	body = models.TextField()
	image = CloudinaryField('image')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10,choices=status_choices,default='draft')
	slug = models.SlugField(unique_for_date='publish')
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	publish = models.DateTimeField(default=timezone.now)
	objects = models.Manager()
	published = PublishedManager()
	tags = TaggableManager()

	class Meta:
		ordering = ('-publish',)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:post_detail_view',args=[self.publish.year,self.publish.month,self.publish.day,self.slug])

class Comment(models.Model):
	name = models.CharField(max_length=20)
	email = models.EmailField()
	post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comment')
	body =models.CharField(max_length=250)
	active = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return self.body