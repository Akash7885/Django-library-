from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime as d
from django.utils import timezone

# Custom User Model
class CustomUser(AbstractUser):
    USER = (
        (1, 'admin'),
        (2, 'students'),
    )
    user_type = models.IntegerField(choices=USER, default=1)
    profile_pic = models.ImageField(upload_to='', blank=True, null=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",
        blank=True
    )

# Category Model
class Category(models.Model):
    catname = models.CharField(max_length=200)
    status = models.CharField(max_length=200, blank=True)
    created_at = models.DateField(auto_now_add=True )   
    updated_at = models.DateField(auto_now=True )  

    def __str__(self):
        return self.catname

# Book Model
class Book(models.Model):
    bookname = models.CharField(max_length=200)
    auther = models.CharField(max_length=200, default=None)
    catid = models.ForeignKey(Category, on_delete=models.CASCADE)
    isbnnum = models.CharField(max_length=200, unique=True)
    price = models.CharField(max_length=200)
    bookimage = models.ImageField(upload_to='', blank=True, null=True)
    created_at = models.DateField(auto_now_add=True )  
    updated_at = models.DateField(auto_now=True )  
    isIssued = models.CharField(max_length=50, default=None)
    expire_at= models.DateField(null=True,default=None)

    def __str__(self):
        return self.bookname

# Student Model
class Student(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email = models.CharField(max_length=50, default=None)  
    studentid = models.CharField(max_length=50, unique=True)
    regdate_at = models.DateField(auto_now_add=True )   
    updated_at = models.DateField(auto_now=True )  

    def __str__(self):
        return self.studentid

# Issued Book Details Model
class Issuedbookdetails(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    stud_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    issued_date = models.DateField(default=timezone.now )  
    return_date = models.DateField(auto_now=True)
    return_status = models.CharField(max_length=50)
    fine = models.DecimalField(max_digits=10, decimal_places=2, default=0)
