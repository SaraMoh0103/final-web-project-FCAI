from django.urls import path
from .import views 
from .views import  delete_book
from .views import book_detail,search_books
from django.contrib.auth.views import LoginView
urlpatterns = [
    path("",views.outhomepage,name='outhomepage'),
    path("services/",views.services,name='services'),
    path("availablebooks/",views.availablebooks,name='availablebooks'),
    path("availablebooksuser/",views.availablebooksuser,name='availablebooksuser'),
    path("book/<int:book_id>/", views.book_detail, name='book_detail'),
    path("bookuser/<int:book_id>/", views.book_detailUser, name='book_detailUser'),
    path("borrow_book/<str:book_id>/", views.borrow_book, name='borrow_book'),
    path("borrowed_books/", views.borrowed_books, name='borrowed_books'),
    path("add_book/", views.add_book, name='add_book'),   
    path('delete_book/<int:book_id>/', delete_book, name='delete_book'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('update_book/<int:book_id>/', views.update_book, name='update_book'),
    path('login',views.loginForm, name='login'),
    path('sign_up',views.sign_up,name='sign_up'),
    path('', views.index, name='index'),
    path('api/books/', views.BookList.as_view(), name='book-list'),
    path('homepage/', views.homepage, name='homepage'),
    path('book/<str:book_id>/', book_detail, name='book_detail'),
    path('homepageUser/', views.homepageUser, name='homepageUser'),
    path('api/search_books/', search_books, name='search_books'),
    path('logout/', views.logout_view, name='logout_page'),
    path('profile/', views.profile_view, name='profile'),
    
]

