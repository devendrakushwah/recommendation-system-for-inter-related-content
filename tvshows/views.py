from django.shortcuts import render
from django.http import HttpResponse
from tvshows import shows_utils

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

def show_detail(request):
    title=request.GET['title']
    show_data=shows_utils.get_show_details(title)
    similar_shows=shows_utils.similar_shows(title)
    data={}
    data['show_data']=show_data
    data['similar_shows']=similar_shows
    #TODO render code
    return HttpResponse(str(data))

def rate_show(request):
    username=str(request.user)
    show_id=request.GET["show_id"]
    rating=request.GET["rating"]
    shows_utils.rate_show(username,show_id,rating)
    #TODO render code
    return HttpResponse("{'message':'success'}")