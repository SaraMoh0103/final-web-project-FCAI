from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_id', 'book_name', 'author', 'category', 'language', 'price', 'description', 'book_img']