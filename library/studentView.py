from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from libraryApp.models import CustomUser,Category,Book,Student,Issuedbookdetails
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def is_admin(user):
    return user.is_superuser==False

@user_passes_test(is_admin,login_url='Login')
def book_details(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all() 
    
    if category_id:
        books = Book.objects.filter(catid=category_id)  
    else:
        books = Book.objects.all() 
 
    context = {
        'books': books,
        'categories': categories,
        'selected_category': category_id 
    }
    return render(request,'student/book-details.html',context)


@user_passes_test(is_admin,login_url='Login')
def stud_issed_books(request):
    stu_admin = request.user
    stu_reg = Student.objects.get(admin=stu_admin)
    
    issuebook_list = Issuedbookdetails.objects.filter(stud_id=stu_reg)

    paginator = Paginator(issuebook_list, 10)  
    page_number = request.GET.get('page')
    try:
        issued_books = paginator.page(page_number)
        
    except PageNotAnInteger:
        issued_books = paginator.page(1)
    except EmptyPage:
        issued_books = paginator.page(paginator.num_pages)

    context = {'issued_books': issued_books,}
    return render(request, 'student/issued_book.html', context)

@login_required(login_url='Login')
def profile(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        # username = request.POST.get('username')
        
        try:
            customuser = CustomUser.objects.get(id = request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            customuser.email = email

            if profile_pic !=None and profile_pic != "":
               customuser.profile_pic = profile_pic
            customuser.save()
            
            messages.success(request,"Your profile has been updated successfully")
            return redirect('profile')

        except:
            messages.error(request,"Your profile updation has been failed")
    return render(request, 'profile.html')