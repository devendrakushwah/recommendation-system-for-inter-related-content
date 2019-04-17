from django.shortcuts import render
from django.http import HttpResponse
from movies import movies_utils
from movies.models import Movie_Rating
from easyRec.utils import similar_items
from django.contrib.auth.decorators import login_required

@login_required
def movie_home(request):
    popular_movies=movies_utils.popular_movies()
    action=movies_utils.top_charts("Action")
    scifi=movies_utils.top_charts("Sci-Fi")
    horror=movies_utils.top_charts("Horror")
    comedy=movies_utils.top_charts("Comedy")
    romance=movies_utils.top_charts("Romance")
    animation = movies_utils.top_charts("Animation")
    personalized=movies_utils.personalized_movies(str(request.user))
    data={}
    data['popular_movies']=popular_movies
    data['action']=action
    data['scifi']=scifi
    data['horror']=horror
    data['comedy']=comedy
    data['romance']=romance
    data['personalized']=personalized
    data['animation']=animation
    data['user']=str(request.user)

    #print(similar_items('m12'))

    #TODO render code
    return render(request,'movies/movies.html',data)

@login_required
def movie_detail(request):
    title=request.GET['title']
    movie_data=movies_utils.get_movie_details(title)
    similar_movies=movies_utils.similar_movies(title)
    data={}
    data['already_rated'] = False
    data['rating_value'] = 0
    qSet=Movie_Rating.objects.filter(username=str(request.user))

    for q in qSet:
        if q.movie_id == movie_data["movie_id"]:
            data['already_rated'] = True
            data['rating_value']=str(q.rating)

    similar_books,similar_tvshows=movies_utils.get_similar_content(movie_data['movie_id'])

    data['movie_data']=movie_data
    data['similar_movies']=similar_movies
    data['similar_books']=similar_books
    data['similar_tvshows']=similar_tvshows

    #TODO render code
    return render(request,'movies/movie_details.html',data)


@login_required
def rate_movie(request):
    username=str(request.user)
    movie_id=request.GET["movie_id"]
    rating=request.GET["rating"]
    movies_utils.rate_movie(username,movie_id,rating)
    #TODO render code
    return HttpResponse("{'message':'success'}")