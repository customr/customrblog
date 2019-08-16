from django.contrib import admin
from django.urls import path, include
from blog import views

app_name = 'blog'
urlpatterns = [
	path('', views.index, name='index-page'),
	path('blog/<str:blog_name>/', views.blog, name='blog'),
	path('post/<int:post_id>/', views.post, name='post'),
	path('posts/', views.get_posts, name='posts'),
	path('posts/topic/<str:topic>', views.get_posts, name='posts_topic'),
	path('user/<int:user_id>/', views.user, name='user'),
	path('users/', views.get_users, name='users'),
	path('help/', views.help, name='help'),
	#````````````````````````CREATION```````````````````````````
	path('newpost/', views.new_post, name='new_post'),
	path('newpost/<str:blog_name>/', views.new_post, name='new_post'),
	path('newblog/', views.new_blog, name='new_blog'),
	#````````````````````````REGISTRATION``````````````````````
	path('register/', views.RegisterFormView.as_view(), name='register'),
	path('register/success/', views.register_success, name='success'),
	path('logout/', views.logout, name='logout'),
	#````````````````````````ACTIONS```````````````````````````
	path('post/<int:post_id>/like', views.like_post, name='like_post'),
	path('post/<int:post_id>/unlike', views.unlike_post, name='unlike_post'),
	path('post/comment/<int:comment_id>/like', views.like_comment, name='like_comment'),
	path('post/comment/<int:comment_id>/unlike', views.unlike_comment, name='unlike_comment'),

]