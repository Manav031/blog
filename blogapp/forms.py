from django import forms
from django.forms import ModelForm
from .models import Blog, BlogCategory
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class BlogForm(ModelForm):
    class Meta:
        model = Blog
        exclude = ['isdelete', 'status', 'user']

class BlogCategoryForm(ModelForm):
    class Meta:
        model = BlogCategory
        fields = '__all__'

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user