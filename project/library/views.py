from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Book , BorrowedBook
from .forms import BookForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from rest_framework import generics
from .serializers import BookSerializer
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout

# Create your views here.
def base(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect('admin_base')
        else:
            return redirect('user_base')
    else:
        return render(request, "base.html")
def services(request):
    form = BookForm()  # Initialize form for adding books
    return render(request, "pages/services.html", {'form': form})

def availablebooks(request):
    books = Book.objects.all()
    return render(request, "pages/availablebooks.html", {'books': books})

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'success'})
        else:
            return JsonResponse({'message': 'error', 'errors': form.errors})
    else:
        return JsonResponse({'message': 'error'})
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('availablebooks')
    return redirect('availablebooks')
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        return render(request, 'pages/edit_book.html', {'book': book})
    return redirect('availablebooks')

def update_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.book_id = request.POST['bookId']
        book.book_name = request.POST['bookName']
        book.author = request.POST['author']
        book.category = request.POST['category']
        book.language = request.POST['language']
        book.price = request.POST['price']
        book.save()
        return redirect('availablebooks')
    return render(request, 'edit_book.html', {'book': book}) 
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, "pages/book.html", {'book': book})

def book_detailUser(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, "pages\Bookdetails_user.html", {'book': book})


# def borrow_book(request, book_id):
#     if request.method == 'POST':
#         book = get_object_or_404(Book, book_id=book_id)
#         if book.available:
#             book.available = False
#             book.save()
#             BorrowedBook.objects.create(book=book)
#             return JsonResponse({'status': 'success'})
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Book not available'}, status=400)
#     return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

# def borrowed_books(request):
#     borrowed_books = BorrowedBook.objects.all()
#     return render(request, "pages/borrowed.html", {'borrowed_books': borrowed_books})


def borrow_book(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, book_id=book_id)
        if book.available:
            book.available = False
            user = request.user
            book.save()
            BorrowedBook.objects.create(book=book, user=user)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Book not available'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def borrowed_books(request):
    borrowed_books = BorrowedBook.objects.filter(user=request.user)
    return render(request, "pages/borrowed.html", {'borrowed_books': borrowed_books})


##############################################
def availablebooksuser(request):
    books = Book.objects.all()
    return render(request, "pages/availablebooksuser.html", {'books': books})


       # redirect him to the home page of admin or student
# def login(request):
#     if request.method =='POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         if not username or not password:
#             error = "Please fill in all fields"
#         else:    
#             user = User.objects.filter(username=username).first()
#             if user:
#                 expected_password = user.password
#                 if check_password(password, expected_password):
#                     if user.is_admin:
#                         return redirect('homepage')
#                     else:
#                         return redirect('homepageUser') 
#                 else:
#                     error = "Please write the correct password"
#             else:
#                 error = "This user name does not exist"
#         return render(request, 'pages/login.html', {'error': error})
#     return render(request, 'pages/login.html')
       

# def sign_up(request):
#     if request.method =='POST':
#         # get the values from the text box
#         username = request.POST.get('username').strip()
#         password = request.POST.get('password').strip()
#         confirmedpass = request.POST.get('conpassword').strip()
#         email = request.POST.get('email').strip()
#         isAdmin = request.POST.get("Is-Admin")
#         errors = []
#         if not username and not password and not confirmedpass and not email:
#             errors.append("Please fill all fields")  

#         if User.objects.filter(username=username).exists():
#             errors.append("This user name is already exist")


#         if password != confirmedpass:
#             errors.append("The passwords do not match")

#         if errors:
#             return render(request,'pages/SignUp.html',{'errors':errors})
        
#         if isAdmin=='on':
#             isAdmin=True
#         else:
#             isAdmin=False

#         hashed_password = make_password(password)
#         registerData = User(username = username , password = hashed_password , email=email, is_admin = isAdmin)
#         registerData.save()
#         return redirect('login')  
#     return render(request,'pages/Signup.html')
def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        confirmedpass = request.POST.get('conpassword').strip()
        email = request.POST.get('email').strip()
        isAdmin = request.POST.get("Is-Admin")
        errors = []
        if not username and not password and not confirmedpass and not email:
             errors.append("Please fill all fields")  

        if User.objects.filter(username=username).exists():
             errors.append("This user name is already exist")


        if password != confirmedpass:
             errors.append("The passwords do not match")

        if errors:
             return render(request,'pages/SignUp.html',{'errors':errors})
        if isAdmin=='on':
            isAdmin=True
        else:
            isAdmin=False
        user = User.objects.create_user(username=username, email=email, password=password) 
        if isAdmin:
            user.is_superuser = True 
        user.save()      
        return redirect('login')  
    return render(request,'pages/Signup.html')
##################################################
def loginForm(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        remember_me = request.POST.get('remember-me')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            if user.is_superuser:
                return redirect('homepage')
            else:
                return redirect('homepageUser')
        else:
            if not username and not password:
                errors = "Please fill all fields"
            else:
                errors = "Invalid username or password"
            return render(request,'pages/Login.html',{'error':errors})
    return render(request,'pages/Login.html')
    

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


def index(request):
    
    latest_books = Book.objects.order_by('-id')[:3]
    context = {
        'latest_books': latest_books,
    }
    return render(request, 'pages/index.html', context)


def homepage(request):
    latest_books = Book.objects.order_by('-id')[:3]
    context = {
        'latest_books': latest_books,
    }
    return render(request, 'pages/homepage.html', context)

def homepageUser(request):
    latest_books = Book.objects.order_by('-id')[:3]
    context = {
        'latest_books': latest_books,
    }
    return render(request, 'pages/homepageUser.html', context)



def outhomepage(request):
     return render(request, 'pages/outhomepage.html')
def search_books(request):
    search_term = request.GET.get('search_term', '').lower()
    search_criteria = request.GET.get('search_criteria', '')

    if search_criteria == 'book_name':
        books = Book.objects.filter(book_name__icontains=search_term)
    elif search_criteria == 'author':
        books = Book.objects.filter(author__icontains=search_term)
    elif search_criteria == 'category':
        books = Book.objects.filter(category__icontains=(search_term))
    else:
        books = Book.objects.none()

    books_data = [{
        'book_name': book.book_name,
        'author': book.author,
        'category': book.category,
        'language': book.language,
        'price': str(book.price),
        'description': book.description,
        'available': book.available,
        'book_img': book.book_img.url if book.book_img else ''
    } for book in books]

    return JsonResponse({'books': books_data})

def logout_view(request):
  if request.user.is_authenticated:
    logout(request)
  return redirect('outhomepage')

@login_required
def profile_view(request):
  context = {}

  # Access user information from the request object
  user = request.user
  context['username'] = user.username
  context['email'] = user.email

  return render(request, 'pages/profile.html', context)

