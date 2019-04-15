from django.urls import path
from books.views import *

app_name='books'

urlpatterns = [
    path('',book_home,name='home'),
    path('detail/',book_detail,name='detail'),
    path('rate/',rate_book,name='rate'),
]