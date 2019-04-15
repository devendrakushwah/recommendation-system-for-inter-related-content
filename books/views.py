from django.shortcuts import render
from django.http import HttpResponse
from books import books_utils

def book_home(request):
    popular_books=books_utils.popular_books()
    action=books_utils.top_charts("Action")
    scifi=books_utils.top_charts("Sci-Fi")
    horror=books_utils.top_charts("Horror")
    comedy=books_utils.top_charts("Comedy")
    history=books_utils.top_charts("Alternate History")
    drama = books_utils.top_charts("Drama")
    personalized=books_utils.personalized_books(str(request.user))
    data={}
    data['popular_books']=popular_books
    data['action']=action
    data['scifi']=scifi
    data['horror']=horror
    data['comedy']=comedy
    data['drama']=drama
    data['history']=history
    data['personalized']=personalized
    #TODO render code
    return render(request,'books/books.html',data)

def book_detail(request):
    title=request.GET['title']
    book_data=books_utils.get_book_details(title)
    similar_books=books_utils.similar_books(title)
    data={}
    data['book_data']=book_data
    data['similar_books']=similar_books
    #TODO render code
    return HttpResponse(str(data))

def rate_book(request):
    username=str(request.user)
    book_id=request.GET["book_id"]
    rating=request.GET["rating"]
    books_utils.rate_book(username,book_id,rating)
    #TODO render code
    return HttpResponse("{'message':'success'}")