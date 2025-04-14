from django.shortcuts import render , redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from libraryApp.models import CustomUser,Category,Book,Student,Issuedbookdetails
from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from datetime import date,timedelta 

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin,login_url='Login')
def add_category(request):
    if request.method == "POST":
        catname = request.POST.get('catname').strip().lower()
        status = request.POST.get('status')

        if Category.objects.filter(catname=catname).exists():
            messages.warning(request,'Category already exist')
            return redirect('add_category')

        else:
            cat =Category(
                catname=catname,
                status=status,
            )
            cat.save()
            messages.success(request,'Category has been added succeesfully!!!')
            return redirect("add_category")
    
    return render(request,'admin/add-category.html')


@user_passes_test(is_admin,login_url='Login')
def add_books(request):
    categories = Category.objects.all()    

    if request.method == "POST":
        bookname = request.POST.get('bookname').strip().lower()
        catid = request.POST.get('catid')
        auther = request.POST.get('auther')
        isbnnum = request.POST.get('isbnnum')
        price = request.POST.get('price')
        bookimage = request.FILES.get('bookimage')

        if Book.objects.filter(bookname=bookname).exists() :
            messages.warning(request,'Book already exist')
            return redirect('add_books')
        
        if Book.objects.filter(isbnnum=isbnnum).exists() :
            messages.warning(request,'ISBN Number already exist')
            return redirect('add_books')

        try:
            catid = int(catid) 
            category = Category.objects.get(id=catid)

        except (Category.DoesNotExist):
            messages.warning(request, 'Invalid category ID')
            return redirect('add_books')
        

        bookinfo = Book(
            bookname=bookname,
            catid=category,
            auther=auther,
            isbnnum=isbnnum,
            price=price,
            bookimage=bookimage,
            isIssued='0'
        )

        bookinfo.save()
        messages.success(request, 'Book info has been added successfully!')
        return redirect('add_books')

    
    context = {
        'categories': categories,
    }
    return render(request, 'admin/add-books.html', context)

@user_passes_test(is_admin,login_url='Login')
def show_category(request):

    cat_list = Category.objects.all()
    paginator = Paginator(cat_list, 10) 
    page_number = request.GET.get('page')
    try:
        categories = paginator.page(page_number)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)

    context = {'categories': categories,}
    
    return render(request,"admin/show-category.html",context)

@user_passes_test(is_admin,login_url='Login')
def delete_category(request,id):
    cat = Category.objects.get(id=id)
    cat.delete()
    messages.success(request,'Record Delete Succeesfully!!!')
    
    return redirect('show_category')

@user_passes_test(is_admin,login_url='Login')
def update_category(request,id):
    cat = Category.objects.get(id=id)
    context = {'cat':cat,}

    return render(request,'admin/update-category.html',context)

@user_passes_test(is_admin,login_url='Login')
def update_category_details(request):
        if request.method == 'POST':
          
          cat_id = request.POST.get('cat_id')
          catname = request.POST.get('catname')
          status = request.POST.get('status')
          category = Category.objects.get(id=cat_id) 
          category.catname = catname
          category.status = status
          category.save()   
          messages.success(request,"Your category detail has been updated successfully")
          return redirect('show_category')
        
        return render(request, 'admin/update-category.html')


@user_passes_test(is_admin,login_url='Login')
def manage_book(request):
    book_list = Book.objects.all().order_by('-id')
    paginator = Paginator(book_list, 10) 

    page_number = request.GET.get('page')
    try:
        books = paginator.page(page_number)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    context = {'books': books,}
    return render(request,"admin/manage-book.html",context)

@user_passes_test(is_admin,login_url='Login')
def delete_books(request,id):
    books = Book.objects.get(id=id)
    books.delete()
    messages.success(request,'Record Delete Succeesfully!!!')
    return redirect('manage_book')

@user_passes_test(is_admin,login_url='Login')
def issue_book(request):
    students = Student.objects.all()
    books = Book.objects.all()
    context = {'books': books,
               'students':students}
    
    return render(request,'admin/issue-book.html',context)

@user_passes_test(is_admin,login_url='Login')
def issue_book(request):
    if request.method == 'POST':
        book_id = request.POST.get('bookid')
        stud_id = request.POST.get('stuid')

        today_Date=date.today()
        expire_date=today_Date+timedelta(days=30)

        try:
            book = Book.objects.get(id=book_id)
            student = Student.objects.get(id=stud_id)
            
            # Create the issued book record
            issued_book = Issuedbookdetails.objects.create(
                book_id=book,  
                stud_id=student,
            )
            issued_book.save()
            book.isIssued = True 
            book.expire_at=expire_date 
            book.save()

            messages.success(request, 'Book issued successfully!')
            return redirect('issue_book') 
        except Exception as e:
            messages.warning(request, f'Error issuing book: {e}')
            return redirect('issue_book') 
    else:
        students = Student.objects.all()
        books = Book.objects.filter(Q(isIssued='0') | Q(isIssued='Return'))
        context = {
            'books': books,
            'students': students
        }
        return render(request, 'admin/issue-book.html', context)
    
@user_passes_test(is_admin,login_url='Login')
def show_issued_book(request):
    
    issuebook_list = Issuedbookdetails.objects.all()
    paginator = Paginator(issuebook_list, 10)  
    
    page_number = request.GET.get('page')
    try:
        issued_books = paginator.page(page_number)
    except PageNotAnInteger:
        issued_books = paginator.page(1)
    except EmptyPage:
        issued_books = paginator.page(paginator.num_pages)

    context = {'issued_books': issued_books,
    }
    return render(request, 'admin/show-issued-book.html', context)


@user_passes_test(is_admin,login_url='Login')
def update_ibstatus(request,id):
    
    iss_books = Issuedbookdetails.objects.get(id=id)

    # issue_Date=iss_books.issued_date
    # return_Date=iss_books.return_date
    exp_date=iss_books.book_id.expire_at
    
    today_Date=date.today()
    total_days=0
    fine=5
    if today_Date < exp_date:
        total_days=0
    else:
        total_days = (today_Date-exp_date).days   

    total_fine=fine*total_days

    context = {'iss_books':iss_books,
               'total_fine':total_fine,
               "total_days":total_days}
    
    return render(request,'admin/update_issue_book_details.html',context)

@user_passes_test(is_admin,login_url='Login')
def update_ibstatus_detail(request):
        if request.method == 'POST':
          book_id = request.POST.get('bookid')
          issbkid = request.POST.get('issbk_id')
          fine = request.POST.get('fine')
         
          try:
            books = get_object_or_404(Book,id=book_id)
            issbks = get_object_or_404(Issuedbookdetails, id=issbkid)
            
            books.isIssued = "Return"
            books.expire_at= None
            issbks.return_status = "Return"
            issbks.fine = fine           

            books.save()   
            issbks.save() 
            messages.success(request,"Issue book detail has been updated successfully")
            return redirect('show_issued_book')

          except (Book.DoesNotExist, Issuedbookdetails.DoesNotExist):
            messages.error(request, "Invalid ID provided for book or issue book")
            return redirect('update_ibstatus')
        return render(request, 'admin/show-issued-book.html')

@user_passes_test(is_admin,login_url='Login')
def reg_users(request):    
    student_list = Student.objects.all()
    paginator = Paginator(student_list, 10)  
    page_number = request.GET.get('page')

    try:
        student_list = paginator.page(page_number)
    except PageNotAnInteger:
        student_list = paginator.page(1)

    except EmptyPage:
        student_list = paginator.page(paginator.num_pages)

    context = {'student_list': student_list,
    }
    return render(request, 'admin/reg-users.html', context)