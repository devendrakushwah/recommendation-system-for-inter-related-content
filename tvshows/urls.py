from django.urls import path
from tvshows.views import *

app_name='tvshows'

urlpatterns = [
    path('',show_home,name='home'),
    path('detail/',show_detail,name='detail'),
    path('rate/',rate_show,name='rate'),
]