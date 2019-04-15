from django.contrib import admin
from books.models import *
# Register your models here.
admin.site.register(Book)
admin.site.register(Book_Rating)