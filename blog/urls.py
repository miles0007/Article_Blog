from django.urls import path
from blog import views
from django.conf import settings
from django.conf.urls.static import static
from blog.feeds import LatestPostsFeed

app_name = 'blog'
urlpatterns = [
		path('',views.post_list_view,name='post_list_view'),
		path('tag/<slug:tag_slug>/',views.post_list_view,name='tag_list'),
		path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail_view,name='post_detail_view'),
		path('<int:post_id>/share/',views.post_share,name='post_share'),
		path('article-moments/',views.moments_view,name='moments_view'),
		path('feed/',LatestPostsFeed(),name='post_feed'),
		path('search-article/',views.post_search,name='post_search'),
		path('tag_list/',views.tag_views,name='all_tags'),
		path('ArticleAbout/',views.about_view,name='about'),

]

urlpatterns +=static(settings.STATIC_URL,document_root= settings.STATIC_ROOT)
urlpatterns +=static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)