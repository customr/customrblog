# Generated by Django 2.2.4 on 2019-08-16 20:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=50, verbose_name='first name')),
                ('last_name', models.CharField(max_length=50, verbose_name='last name')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('date_of_birth', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, unique=True, verbose_name='Name')),
                ('rating', models.IntegerField(default=0, verbose_name='Rating')),
                ('author', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(blank=True, max_length=50, verbose_name='Topic')),
                ('title', models.CharField(blank=True, max_length=50, verbose_name='Title')),
                ('text', models.TextField(blank=True, max_length=5000, verbose_name='Text')),
                ('rating', models.IntegerField(default=0, verbose_name='Rating')),
                ('date_published', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Date published')),
                ('author', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('blog', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Blog')),
                ('liked_users', models.ManyToManyField(default=None, related_name='liked_post', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, max_length=1000, verbose_name='Text')),
                ('rating', models.IntegerField(blank=True, default=0, verbose_name='Rating')),
                ('date_published', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Date published')),
                ('author', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('liked_users', models.ManyToManyField(default=None, related_name='liked_comments', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Post')),
            ],
        ),
    ]
