"""
URL configuration for library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views,adminView,studentView

urlpatterns = [
    path('',views.index),
    path('admin/', admin.site.urls),
    path('Login', views.Login, name='Login'),
    path('doLogout', views.doLogout, name='doLogout'),
    path('doLogin', views.doLogin, name='doLogin'),
    path('register', views.register, name='register'),
    path('Dashboard', views.Dashboard, name='Dashboard'),
    path('add_category', adminView.add_category, name='add_category'),
    path('show_category', adminView.show_category, name='show_category'),
    path('delete_category/<str:id>', adminView.delete_category, name='delete_category'),
    path('update_category/<str:id>', adminView.update_category, name='update_category'),
    path('update_category_details', adminView.update_category_details, name='update_category_details'),
    path('add_books', adminView.add_books, name='add_books'),
    path('manage_book', adminView.manage_book, name='manage_book'),
    path('book_details', studentView.book_details, name='book_details'),
    path('delete_books/<str:id>', adminView.delete_books, name='delete_books'),
    path('issue_book', adminView.issue_book, name='issue_book'),
    path('show_issued_book', adminView.show_issued_book, name='show_issued_book'),
    path('update_ibstatus/<str:id>', adminView.update_ibstatus, name='update_ibstatus'),
    path('update_ibstatus_detail', adminView.update_ibstatus_detail, name='update_ibstatus_detail'),
    path('reg_users', adminView.reg_users, name='reg_users'),
    path('change_password', views.change_password, name='change_password'),

    path('stud_issed_books', studentView.stud_issed_books, name='stud_issed_books'),
    path('profile', studentView.profile, name='profile'),
    path('search_book',views.search_book,name='search_book')

]
