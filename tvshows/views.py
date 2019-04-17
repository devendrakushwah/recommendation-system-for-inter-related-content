from django.shortcuts import render
from django.http import HttpResponse
from tvshows import shows_utils
from tvshows.models import Show_Rating
from django.contrib.auth.decorators import login_required

@login_required
def show_home(request):
    popular_shows=shows_utils.popular_shows()
    action=shows_utils.top_charts("Action")
    scifi=shows_utils.top_charts("Sci-Fi")
    horror=shows_utils.top_charts("Horror")
    comedy=shows_utils.top_charts("Comedy")
    romance=shows_utils.top_charts("Romance")
    crime = shows_utils.top_charts("Crime")
    drama=shows_utils.top_charts('Drama')
    personalized=shows_utils.personalized_shows(str(request.user))
    data={}
    data['popular_shows']=popular_shows
    data['action']=action
    data['scifi']=scifi
    data['horror']=horror
    data['comedy']=comedy
    data['romance']=romance
    data['crime'] = crime
    data['drama'] = drama
    data['personalized']=personalized
    #TODO render code
    return render(request,'tvshows/tvshows.html',data)

@login_required
def show_detail(request):
    title=request.GET['title']
    show_data=shows_utils.get_show_details(title)
    similar_shows=shows_utils.similar_shows(title)
    data={}

    data['already_rated'] = False
    data['rating_value'] = 0
    qSet = Show_Rating.objects.filter(username=str(request.user))

    for q in qSet:
        if q.show_id == show_data["show_id"]:
            data['already_rated'] = True
            data['rating_value'] = str(q.rating)

    similar_movies, similar_books = shows_utils.get_similar_content(show_data['show_id'])

    data['show_data']=show_data
    data['similar_tvshows']=similar_shows
    data['similar_movies']=similar_movies
    data['similar_books']=similar_books
    data['user']=str(request.user)

    #TODO render code
    return render(request,'tvshows/tvshow_details.html',data)

@login_required
def rate_show(request):
    username=str(request.user)
    show_id=request.GET["show_id"]
    rating=request.GET["rating"]
    shows_utils.rate_show(username,show_id,rating)
    #TODO render code
    return HttpResponse("{'message':'success'}")