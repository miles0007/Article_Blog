from django.contrib import admin
from blog.models import Post,Comment
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('title','created','status','author')
	list_filter = ('title','author','created')
	search_fields = ('title','body')
	prepopulated_fields = {'slug':('title',)}
	date_hierarchy = ('publish')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('name','email','post','created')
	list_filter = ('name','post','created')
	search_fields = ('name','body')
