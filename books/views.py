from django.shortcuts import render
from django.http import HttpResponse
from books import books_utils
from books.models import Book_Rating
from django.contrib.auth.decorators import login_required

@login_required
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

@login_required
def book_detail(request):
    title=request.GET['title']
    book_data=books_utils.get_book_details(title)
    similar_books=books_utils.similar_books(title)
    data={}

    data['already_rated'] = False
    data['rating_value'] = 0
    qSet=Book_Rating.objects.filter(username=str(request.user))

    for q in qSet:
        if q.book_id == book_data["book_id"]:
            data['already_rated'] = True
            data['rating_value']=str(q.rating)


    similar_movies,similar_tvshows = books_utils.get_similar_content(book_data['book_id'])

    data['book_data']=book_data
    data['similar_books']=similar_books
    data['similar_movies'] = similar_movies
    data['similar_tvshows'] = similar_tvshows
    data['user']=str(request.user)

    #TODO render code
    return render(request,'books/book_details.html',data)

@login_required
def rate_book(request):
    username=str(request.user)
    book_id=request.GET["book_id"]
    rating=request.GET["rating"]
    books_utils.rate_book(username,book_id,rating)
    #TODO render code
    return HttpResponse("{'message':'success'}")