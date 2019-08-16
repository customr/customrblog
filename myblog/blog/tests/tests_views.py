from django.test import TestCase, Client
from django.urls import reverse

from blog.models import Author, Blog, Post, Comment
from .tests_models import create_post, create_blog, create_author

client = Client()

class IndexViewTest(TestCase):

	def test_index(self):
		response = self.client.get(reverse('blog:index-page'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Blogs')
		self.assertQuerysetEqual(response.context['blogs'], [])