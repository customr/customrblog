from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.views.generic import edit
from django.db.models import F
from django.contrib.auth.decorators import login_required

from blog.models import MyUser, Blog, Post, Comment
from blog.forms import UserCreationForm, BlogForm, PostForm, CommentForm


class RegisterFormView(edit.FormView):
    form_class = UserCreationForm
    success_url = "success"
    template_name = "registration/registration.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)




@login_required(login_url='login')
def new_blog(request):
	if request.method == 'POST':
		form = BlogForm(request.POST)
		if form.is_valid():
			blog = form.save(commit=False)
			blog.author = request.user
			blog.date_published = timezone.now()
			blog.save()
			return HttpResponseRedirect(reverse('blog:blog', args=(blog.name, )))

	else:
		form = BlogForm()
		return render(request, 'blog/new_blog.html', {'form': form})

@login_required(login_url='login')
def new_post(request, blog_name=None):
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)

			if blog_name:
				post.blog = get_object_or_404(Blog, name__iexact=blog_name)

			post.author = request.user
			post.date_published = timezone.now()
			post.save()
			return HttpResponseRedirect(reverse('blog:post', args=(post.id, )))

	else:
		if blog_name:
			form = PostForm(initial={'blog': get_object_or_404(Blog, name__iexact=blog_name)})
		else:
			form = PostForm()
			
		return render(request, 'blog/new_post.html', {'form': form})


def index(request):
	blogs = Blog.objects.all()
	context = {'blogs': blogs}
	return render(request, 'blog/index.html', context)

def blog(request, blog_name):
	blog = get_object_or_404(Blog, name__iexact=blog_name)
	posts = blog.post_set.all()
	context = {
		'blog': blog,
		'posts': posts
		}
	return render(request, 'blog/blog_detail.html', context)

def post(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	comments = post.comment_set.all()

	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.author = request.user
			comment.date_published = timezone.now()
			comment.save()
			return HttpResponseRedirect(reverse('blog:post', args=(comment.post.id, )))

	else:
		form = CommentForm()
		context = {
			'post': post,
			'comments': comments,
			'form': form
		}
		return render(request, 'blog/post_detail.html', context)



def get_posts(request, topic=None):
	posts = Post.objects.all()
	
	if topic is not None:
		posts = posts.filter(topic__iexact=topic)

	context = {
		'posts': posts,
		'topic': topic
		}
	return render(request, 'blog/post.html', context)

def user(request, user_id):
	user = get_object_or_404(MyUser, pk=user_id)
	blogs = Blog.objects.filter(author=user)
	posts = Post.objects.filter(author=user)

	context = {
		'thisuser': user,
		'posts': posts,
		'blogs': blogs
		}
	return render(request, 'blog/user_detail.html', context)

def get_users(request):
	users = MyUser.objects.all()
	context = {'users': users}
	return render(request, 'blog/users.html', context)

def help(request):
	blog = Blog.objects.order_by("?").first()
	post = Post.objects.order_by("?").first()
	topic = None
	author = None

	if not blog:
		blog = None

	if post:
		topic = post.topic
		author = post.author.id
		post = post.id

	else:
		post = None

	context = {
		'blog': blog.name,
		'post': post,
		'topic': topic,
		'author': author
	}
	return render(request, 'blog/help.html', context)

@login_required(login_url='accounts/login/')
def register_success(request):
	return render(request, 'registration/registration_success.html', {})

@login_required(login_url='accounts/login/')
def logout(request):
	return render(request, 'registration/logout.html', {})




#`````````````````````````````ACTIONS```````````````````````````````````
@login_required(login_url='accounts/login/')
def like_post(request, post_id):
	post = get_object_or_404(Post, pk=post_id)

	if request.META['REMOTE_ADDR'] not in post.liked_users:
		post.liked_users.append(request.META['REMOTE_ADDR'])
		Post.objects.filter(pk=post.id).update(rating=F('rating') + 1)
		Blog.objects.filter(pk=post.blog.id).update(rating=F('rating') + 1)

	return HttpResponseRedirect(reverse('blog:post', args=(post.id, )))

@login_required(login_url='accounts/login/')
def like_comment(request, comment_id):
	comment = get_object_or_404(Comment, pk=comment_id)

	if request.META['REMOTE_ADDR'] not in comment.liked_users:
		comment.liked_users.append(request.META['REMOTE_ADDR'])
		Comment.objects.filter(pk=comment.id).update(rating=F('rating') + 1)
		Blog.objects.filter(pk=comment.post.blog.id).update(rating=F('rating') + 1)

	return HttpResponseRedirect(reverse('blog:post', args=(comment.post.id, )))

@login_required(login_url='accounts/login/')
def unlike_post(request, post_id):
	post = get_object_or_404(Post, pk=post_id)

	if request.META['REMOTE_ADDR'] in post.liked_users:
		post.liked_users.remove(request.META['REMOTE_ADDR'])
		Post.objects.filter(pk=post.id).update(rating=F('rating') - 1)
		Blog.objects.filter(pk=post.blog.id).update(rating=F('rating') - 1)

	return HttpResponseRedirect(reverse('blog:post', args=(post.id, )))


@login_required(login_url='accounts/login/')
def unlike_comment(request, comment_id):
	comment = get_object_or_404(Comment, pk=comment_id)

	if request.META['REMOTE_ADDR'] in comment.liked_users:
		comment.liked_users.remove(request.META['REMOTE_ADDR'])
		Comment.objects.filter(pk=comment.id).update(rating=F('rating') - 1)
		Blog.objects.filter(pk=comment.post.blog.id).update(rating=F('rating') - 1)

	return HttpResponseRedirect(reverse('blog:post', args=(post.id, )))
