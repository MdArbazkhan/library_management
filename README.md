# Library management system
### backend code documentation

### 1. Django project configuration - `settings.py`
#### 1.1 Setting up MySQL database
```
DATABASES = {
    'default': {
        'ENGINE'  : 'django.db.backends.mysql', 
        'NAME'    : 'mytestdb',                  
        'USER'    : 'test',                    
        'PASSWORD': 'Secret_1234',              
        'HOST'    : 'localhost',                
        'PORT'    : '3306',
    }
}
```
Referene used to setup MYSQL database on Ubuntu machine
- https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04
- https://dev.to/sm0ke/how-to-use-mysql-with-django-for-beginners-2ni0

#### 1.2 Add django app to `INSTALLED_APPS`
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'manage_lib',
]
```
### 2. Root `urls.py`
```
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('manage_lib.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```
### 2. App - `manage_lib` - `urls.py`
```
urlpatterns = [
    path('', views.landingpage, name='landing-page'),
    path('signupp', views.signuppage, name='signup-page'),
    path('login', views.loginpage, name='login-page'),
    path('logout', views.logoutpage, name='logout-page'),
    path('admin_dashboard', views.dashboard, name='admin-dashboard-page'),
    path('addbook', views.addnew, name='add-new-page'),
    path('updatebook/<str:book_id>', views.updatebook, name='update-book-page'),
    path('deletebook/<str:book_id>', views.deletebook, name='delete-book-page'),
]
```
### 2. App - `manage_lib` - `views.py`
#### 2.1 Admin Signup
```
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
```
#### 2.2 Admin Login
```

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
```
#### 2.3 Admin Logout
```
def logoutpage(request):
    if request.method=="GET":
        return redirect('admin-dashboard-page')
    else:
        logout(request)
        return redirect('landing-page')
```
#### 2.4 Add new book
```
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
```
#### 2.5 Update new book
```

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
```
#### 2.6 Delete book
```

def deletebook(request,book_id):
    if request.method == "GET":
        return redirect('admin-dashboard-page')
    else:
        book_obj = Books.objects.get(book_id=book_id)
        book_obj.delete()
        return redirect('admin-dashboard-page')
```
#### 2.7 Book list or to laod dashboard page after login
```

def dashboard(request):
    if request.method == "GET":
        all_obj = Books.objects.all()
        return render(request, 'manage_lib/dashboard.html',{'all_obj':all_obj})
```
### 3. App - `manage_lib` - `urls.py`
#### 3.1 Books model
We have just one model in `manage_lib` app to store books details to database.
```
class Books(models.Model):
    book_id = models.CharField(max_length=15,default="")
    book_name = models.CharField(max_length=40,default="")
    author_name = models.CharField(max_length=20,default="")
```
Here `book_id` is being used as a unique identifier to perform CRUD operation.

# Screenshots
#### signup page
<img src='https://github.com/MdArbazkhan/library_management/blob/main/manage_lib/static/manage_lib/assets/signup_page.png' />

#### login page
<img src='https://github.com/MdArbazkhan/library_management/blob/main/manage_lib/static/manage_lib/assets/login_page.png' />

#### login error alert page
<img src='https://github.com/MdArbazkhan/library_management/blob/main/manage_lib/static/manage_lib/assets/login_error_alert.png' />

#### book list page
<img src='https://github.com/MdArbazkhan/library_management/blob/main/manage_lib/static/manage_lib/assets/book_list_dashboard.png' />

#### add book page
<img src='https://github.com/MdArbazkhan/library_management/blob/main/manage_lib/static/manage_lib/assets/add_book_Page.png' />

#### update and delete book page
<img src='https://github.com/MdArbazkhan/library_management/blob/main/manage_lib/static/manage_lib/assets/update_delete_book_page.png' />
