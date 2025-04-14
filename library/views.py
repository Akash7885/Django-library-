from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required  
from django.contrib.auth import authenticate, login,logout
from libraryApp.models import CustomUser,Category,Book,Student
from django.contrib import messages
import random


def index(request):    
       return render(request,'index.html')

def Login(request):
    if request.user.is_authenticated:
        print("-----------------------")
        return redirect('Dashboard')

    return render(request,"login.html")

def doLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1' or user_type == 1:  
                return redirect('Dashboard')
            elif user_type == '2' or user_type == 2:  
                return redirect('book_details')
        else:
            messages.warning(request, 'Username or Password is not valid')
        
        return redirect('Login')

    else:
        messages.warning(request, 'Invalid request method')
        return redirect('Login')


def register(request):
    if request.method == "POST":
        random_digits = random.randint(1000, 9999)
        studentid = f"SS{random_digits}"
        pic = request.FILES.get('pic')
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request,'Email already exist')
            return redirect('register')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request,'Username already exist')
            return redirect('register')
        
        else:
            user = CustomUser(
               first_name=first_name,
               username=username,
               email=email,
               
               user_type=2,
               profile_pic = pic,
            ) 
            user.set_password(password)
            user.save()

            student = Student(
                admin = user,
                studentid= studentid, 
                email=email,
            )
            student.save() 
                    
            messages.success(request,'Signup Successfully')
            return redirect('Login')

    return render(request,'register.html')

@login_required(login_url='Login')
def Dashboard(request):
    cat_count = Category.objects.all().count()
    book_count = Book.objects.filter(catid__status="Active").count()
    issbook_count = Book.objects.filter(isIssued=True).count()  
    regusers_count = Student.objects.all().count()
    retbook_count = Book.objects.filter(isIssued='Return').count()

    context = {
        'cat_count': cat_count,
        'book_count': book_count,
        'issbook_count': issbook_count,
        'regusers_count': regusers_count,
        'retbook_count' : retbook_count,
    } 
    return render(request, 'dashbord.html', context) 

def doLogout(request):
    logout(request)
    return redirect('Login')


@login_required(login_url='/')
def change_password(request):
    context ={}
    ch = CustomUser.objects.filter(id = request.user.id)
     
    if len(ch)>0:
            data = CustomUser.objects.get(id = request.user.id)
            context["data"]:data           
    if request.method == "POST":        
        current = request.POST["cpwd"]
        new_pas = request.POST['npwd']
        user = CustomUser.objects.get(id = request.user.id)
        un = user.username
        check = user.check_password(current)
        if check == True:
          user.set_password(new_pas)
          user.save()
          messages.success(request,'Password Change  Succeesfully!!!')
          user = CustomUser.objects.get(username=un)
          login(request,user)
        else:
          messages.success(request,'Current Password wrong!!!')
          return redirect("change_password")
    return render(request,'change-password.html')


def search_book(request):
    if request.method == 'POST':
        query=request.POST.get('query')

        if query == '':
            messages.warning(request,'Please Enter Valid Book Name')
            return redirect('search_book')
        else:
            search_b=Book.objects.filter(bookname__icontains=query)
            print(search_b)
            
            if search_b :  
                pass
            else:
                messages.warning(request,"Book is not Available")

            context={"search_b":search_b}
            return render(request,'search-book.html',context) 

    return render(request,'search-book.html') 