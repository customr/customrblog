from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from blog.models import MyUser, Blog, Post, Comment

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('username', 'first_name', 'last_name', 'email', 'date_of_birth')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'date_of_birth', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ('name',)


class PostForm(forms.ModelForm):

    text = forms.CharField(label='Body:', max_length=5500, 
        widget=forms.Textarea(attrs={'rows':'15 ', 'cols':'180'}))

    class Meta:
        model = Post
        fields = ('blog', 'topic', 'title', 'text')


class CommentForm(forms.ModelForm):

    text = forms.CharField(label='Leave comment:', max_length=1000, 
        widget=forms.Textarea(attrs={'rows':'3', 'cols':'180'}))

    class Meta:
        model = Comment
        fields = ('text',)
