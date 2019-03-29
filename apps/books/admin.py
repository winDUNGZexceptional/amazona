from django.contrib import admin

from apps.books.models import Book, Review, Author
# Register your models here.


admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Author)