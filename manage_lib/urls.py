from django.urls import path
from . import views

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