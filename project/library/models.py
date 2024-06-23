from django.db import models

# Create your models here.
class Book(models.Model):
    book_id = models.CharField(max_length=10, unique=True)
    book_name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    book_img = models.ImageField(upload_to='book_images/', blank=True, null=True)
    available = models.BooleanField(default=True)  # Add availability field

    def __str__(self):
        return self.book_name
    
class BorrowedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=100)    
    def __str__(self):
        return f"{self.book.book_name} borrowed on {self.borrowed_date}"
      
        