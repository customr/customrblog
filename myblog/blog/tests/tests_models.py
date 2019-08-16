import datetime

from django.test import TestCase
from django.utils import timezone

from blog.models import Author, Post, Blog, Comment


def create_author(**kw):
	authors = Author.objects.all()

	if len(authors) == 0 or len(kw) != 0:
		return Author('Test', 'Test', 'test@mail.ru', '1999-02-02', **kw)
	else:
		return authors[0]

def create_blog(**kw):
	blogs = Blog.objects.all()

	if len(blogs) == 0 or len(kw) != 0:
		return Blog(create_author(), 'test', **kw)
	else:
		return blogs[0]

def create_post(**kw):
	posts = Post.objects.all()

	if len(posts) == 0 or len(kw) != 0:
		return Post(create_blog(), create_author(), 'test', 'test', 'test', **kw)
	else:
		return posts[0]

def create_comment(**kw):
	comments = Comment.objects.all()

	if len(comments) == 0 or len(kw) != 0:
		return Comment(create_author(), 'test', 'test')
	else:
		return comments[0]


class AuthorModelTest(TestCase):
	author1 = create_author()
	author2 = create_author(rating=5)

	self.assertEqual(author2.rating, 5)

class BlogModelTest(TestCase):
	blog1 = create_blog()
	blog2 = create_blog(rating=5)

	self.assertEqual(blog2.rating, 5)

class PostModelTest(TestCase):
	post1 = create_post()
	post2 = create_post(rating=5)

	self.assertEqual(post2.rating, 5)

class CommentModelTest(TestCase):
	comment1 = create_comment()
	comment2 = create_comment(rating=5)

	self.assertEqual(comment2.rating, 5)
