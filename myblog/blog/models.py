import datetime
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser



class MyUserManager(BaseUserManager):
	def create_user(self, username, first_name, last_name, email, date_of_birth, password=None):
		if not email:
			raise ValueError('Users must have an email address')

		if not username:
			raise ValueError('User must have an username')

		if not first_name or not last_name:
			raise ValueError('Users must have a fullname')

		if not password:
			raise ValueError('Users must have a password')

		user = self.model(
			username=username,
			first_name=first_name,
			last_name=last_name,
			email=self.normalize_email(email),
			date_of_birth=date_of_birth,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, first_name, last_name, email, date_of_birth, password):
		user = self.create_user(
			username=username,
			first_name=first_name,
 			last_name=last_name,
			email=email,
			password=password,
			date_of_birth=date_of_birth,
		)
		user.is_admin = True
		user.save(using=self._db)
		return user


class MyUser(AbstractBaseUser):
	username = models.CharField('username', max_length=50, unique=True)
	first_name = models.CharField('first name', max_length=50)
	last_name = models.CharField('last name', max_length=50)
	email = models.EmailField(
		verbose_name='email address',
		max_length=255,
		unique=True,
	)
	date_of_birth = models.DateField()
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects = MyUserManager()

	USERNAME_FIELD = 'username'
	EMAIL_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'date_of_birth']

	def __str__(self):
		return self.username

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	def get_absolute_url(self):
		return reverse('blog:user', args=[str(self.id)])

	@property
	def is_staff(self):
		return self.is_admin


class Blog(models.Model):
	author = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=True)
	name = models.CharField('Name', max_length=50, blank=True, unique=True)
	rating = models.IntegerField('Rating', default=0)

	def __str__(self):
		return f'Blog #{self.id} {self.name}'

	def get_absolute_url(self):
		return reverse('blog:blog', args=[str(self.name)])


class Post(models.Model):
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE, blank=True)
	author = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=True)
	topic = models.CharField('Topic', max_length=50, blank=True)
	title = models.CharField('Title', max_length=5500, blank=True)
	text = models.TextField('Text', max_length=00, blank=True)
	rating = models.IntegerField('Rating', default=0)
	date_published = models.DateTimeField('Date published', default=timezone.now, blank=True)

	liked_users = []

	def __str__(self):
		return f'#{self.id} {self.title}'

	def get_absolute_url(self):
		return reverse('blog:post', args=[str(self.id)])


class Comment(models.Model):
	author = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=True)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True)
	text = models.TextField('Text', max_length=1000, blank=True)
	rating = models.IntegerField('Rating', default=0, blank=True)
	date_published = models.DateTimeField('Date published', default=timezone.now, blank=True)

	liked_users = []

	def __str__(self):
		return f'Comment {self.id}'

	def get_absolute_url(self):
		return reverse('blog:post', args=[str(self.post.id)])