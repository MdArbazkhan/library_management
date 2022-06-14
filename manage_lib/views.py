from venv import create
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .models import Books
import uuid 


# Create your views here.
def landingpage(request):
    return render(request, 'manage_lib/landing.html')

def signuppage(request):
    alert_flag = False
    alert_message = ""
    if request.method == 'GET':
        return render(request, 'manage_lib/signup.html',{'alert_flag':alert_flag,'alert_message':alert_message})
    else:
        email_id = request.POST['email_id']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1!= password2:
            alert_flag = True
            alert_message = "Password didn't match"
            return render(request, 'manage_lib/signup.html',{'alert_flag':alert_flag,'alert_message':alert_message})
        emailresult = User.objects.filter(email=email_id)
        if len(emailresult)>0:
            alert_flag = True
            alert_message = "Email id already exists"
            return render(request, 'manage_lib/signup.html',{'alert_flag':alert_flag,'alert_message':alert_message})
        user_object = User(username=email_id,email=email_id,password=password1)
        user_object.save()
        return redirect('login-page')



def loginpage(request):
    alert_flag = False
    alert_message = ""
    if request.method == 'GET':
        return render(request, 'manage_lib/login.html',{'alert_flag':alert_flag,'alert_message':alert_message})
    else:
        email_id = request.POST['email_id']
        password1 = request.POST['password1']
        try:
            user = User.objects.get(email=email_id, password=password1)
        except:
            user = None
        print(user)

        if user is not None:
            login(request, user)
            return redirect("admin-dashboard-page")
            # if request.user.is_superuser:
            #     return redirect("/admin-dashboard-page")
            # else:
            #     pass
        else:
            alert_flag = True
            alert_message = "Enter a valid email or password"
            return render(request, 'manage_lib/login.html',{'alert_flag':alert_flag,'alert_message':alert_message})


def logoutpage(request):
    if request.method=="GET":
        return redirect('admin-dashboard-page')
    else:
        logout(request)
        return redirect('landing-page')


def addnew(request):
    if request.method == "GET":
        return render(request, 'manage_lib/add-books.html')
    else:
        book_name = request.POST['book']
        author_name = request.POST['author']
        book_id = uuid.uuid4().hex[:15].upper()
        new_obj = Books(book_id=book_id, book_name=book_name,author_name=author_name)
        new_obj.save()
        return redirect('admin-dashboard-page')


def updatebook(request,book_id):
    if request.method == "GET":
        try:
            book_obj = Books.objects.get(book_id=book_id)
        except:
            return redirect('admin-dashboard-page')
        return render(request, 'manage_lib/update-book.html',{'book_obj':book_obj})
    else:
        book = request.POST['book']
        author = request.POST['author']
        book_obj = Books.objects.get(book_id=book_id)
        book_obj.book_name = book
        book_obj.author_name = author
        book_obj.save()
        return redirect('/updatebook/'+book_id)


def deletebook(request,book_id):
    if request.method == "GET":
        return redirect('admin-dashboard-page')
    else:
        book_obj = Books.objects.get(book_id=book_id)
        book_obj.delete()
        return redirect('admin-dashboard-page')


def dashboard(request):
    if request.method == "GET":
        all_obj = Books.objects.all()
        return render(request, 'manage_lib/dashboard.html',{'all_obj':all_obj})
    
        