from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from blog.models import MyUser, Blog, Post, Comment
from blog.forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'password1', 'password2')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


class BlogAdmin(admin.ModelAdmin):
	fields = ['author', 'name']
	list_display = ['name', 'author', 'rating']
	list_filter = ['rating']

class PostAdmin(admin.ModelAdmin):
	fields = ['topic', 'rating', 'blog', 'author']
	list_display = ['rating', 'blog', 'topic', 'title', 'author']
	list_filter = ['rating', 'blog', 'topic']

class CommentAdmin(admin.ModelAdmin):
	fields = ['author', 'post', 'text']
	list_display = ['rating', 'post']
	list_filter = ['rating', 'post']

admin.site.register(MyUser, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)