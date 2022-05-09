from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from .forms import BlogForm, BlogCategoryForm, UserCreateForm
from .models import Blog, BlogCategory
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .decorators import allowed_users

from django.db.models import Q

import time

from django.core.paginator import Paginator
# Create your views here.
class ViewBlog(View):
    form_class = BlogForm
    template_name = 'createblog.html'

    @method_decorator(login_required(login_url='/'))
    @method_decorator(allowed_users(allowed_roles=["admin_blog"]))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        if action == "create-blog":
            form = self.form_class()
            return render(request, self.template_name, context={
                "form":form,
                "action":"create-blog-db"
            })

        if action == "create-blog-db":
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                u = form.save(commit=False)
                u.user = request.user
                u.save()
                return redirect('index')

        if action == "create-category":
            form = BlogCategoryForm()
            return render(request, 'createcategory.html', context={
                "form":form,
                "action": "create-category-db",
                "formaction":action
            })

        if action == "create-category-db":
            form = BlogCategoryForm(request.POST)

            if BlogCategory.objects.filter(category=request.POST['category']).exists():
                return HttpResponse('error already exists')

            if form.is_valid():
                form.save()
                return redirect('index')

        if action == "update-category":
            record = request.POST['record']
            data = BlogCategory.objects.get(blogcategoryid=int(record)-settings.MYVAL)
            form = BlogCategoryForm(instance=data)
            return render(request, 'createcategory.html', context={
                "form":form,
                "record":record,
                "action":"update-category-db"
            })

        if action == "update-category-db":
            record = request.POST['record']
            data = BlogCategory.objects.get(blogcategoryid=int(record)-settings.MYVAL)
            form = BlogCategoryForm(request.POST, instance=data)

            if BlogCategory.objects.filter(category=request.POST['category']).exclude(blogcategoryid=int(record)-settings.MYVAL).exists():
                return HttpResponse('error already exists')

            if form.is_valid():
                form.save()
                return redirect('viewCategory')

        if action == "delete-category":
            record = request.POST['record']
            data = BlogCategory.objects.get(blogcategoryid=int(record)-settings.MYVAL)
            data.delete()
            return redirect('viewCategory')

        if action == "update-blog":
            record = request.POST['record']
            data = Blog.objects.get(id=int(record)-settings.MYVAL)
            form = BlogForm(instance=data)
            return render(request, 'createBlog.html', context={
                "form":form,
                "record":record,
                "action":"update-blog-db",
                "formaction":action
            })

        if action == "update-blog-db":
            record = request.POST['record']
            data = Blog.objects.get(id=int(record)-settings.MYVAL)
            form = BlogForm(request.POST, request.FILES, instance=data)
            
            if Blog.objects.filter(title=request.POST['title']).exclude(id=int(record)-settings.MYVAL).exists():
                return HttpResponse('error already exists')
            
            if form.is_valid():
                form.save()
                return redirect('index')

        if action == "delete-blog":
            record = request.POST['record']
            data = Blog.objects.get(id=int(record)-settings.MYVAL)
            data.isdelete = True
            data.save()
            return redirect('index')

    def get(self, request, *args, **kwargs):
        data = BlogCategory.objects.all()
        for i in data:
            i.blogcategoryid += settings.MYVAL
        return render(request, 'view-category.html', context={
            "data":data
        })


class IndexView(ListView):
    template_name = 'index.html'
    model = Blog

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, request, **kwargs):
        context = Blog.objects.filter(Q(status="Approve") & Q(isdelete=False)).order_by('id')
        return context

    def get(self, request, *args, **kwargs):
        groups = [i.name for i in request.user.groups.all()]
        data = self.get_context_data(request)
        # extra aded start
        p = Paginator(data, 2)
        page_number = request.GET.get('page')
        page_obj = p.get_page(page_number)
        # extra aded end
        for i in page_obj:
            i.id += settings.MYVAL
        context = {
            "blogs":data,
            "group": groups,
            "page_obj": page_obj,
        }
        time.sleep(2)
        return render(request, self.template_name, context)

@login_required(login_url='/')
def checkData(request):
    recv_data = request.GET.get('data', None)
    data = BlogCategory.objects.filter(category=recv_data)
    if data.exists():
        return JsonResponse({"error":"already exist"})
    return JsonResponse({"success":"not exist"})

@login_required(login_url='/')
def checkBlog(request):
    recv_data = request.GET.get('data', None)
    data = Blog.objects.filter(title=recv_data)
    if data.exists():
        return JsonResponse({"error":"already exist"})
    return JsonResponse({"success":"not exist"})

class SignupView(View):
    form_class = UserCreateForm
    template_name = 'signup.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={
            "form":form
        })

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Successfully registered!")
            return redirect('index')
        else:
            return HttpResponse("invalid info try again")

class LoginView(View):
    template_name = 'login.html'
    form_class = AuthenticationForm

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, context={
            "form":form
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('index')

def Logout(request):
    logout(request)
    return redirect('login')

class UserView(View):
    template_name = "readmore.html"
    def post(self, request, *args, **kwargs):
        print(request.POST)
        action = request.POST.get('action', None)
        
        if action == "read-more":
            record = request.POST.get('record', None)
            blog = Blog.objects.get(id=int(record)-settings.MYVAL)
            return render(request, self.template_name, context={
                "blog":blog
            })