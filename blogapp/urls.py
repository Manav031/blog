from django.urls import path
from . import views
urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', views.Logout, name='logout'),
    path('blog/', views.IndexView.as_view(), name="index"),
    path('create/', views.ViewBlog.as_view(), name="createBlog"),
    path('createCategory/', views.ViewBlog.as_view(), name="createCategory"),
    path('viewCategory/', views.ViewBlog.as_view(), name="viewCategory"),
    path('updateCategory/', views.ViewBlog.as_view(), name="updateCategory"),
    path('deleteCategory/', views.ViewBlog.as_view(), name="deleteCategory"),
    path('deleteBlog/', views.ViewBlog.as_view(), name="deleteBlog"),
    path('updateBlog/', views.ViewBlog.as_view(), name="updateBlog"),
    path('ajaxcheckcategory/', views.checkData, name="checkcategory"),
    path('ajaxcheckblog/', views.checkBlog, name="checkblog"),
    path('readmore/', views.UserView.as_view(), name="readMore")
]