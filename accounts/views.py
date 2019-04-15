from django.shortcuts import render
from django.http import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth import login

class MySignUpView(View):
    form_class = UserCreationForm
    template_name = 'accounts/sign_up.html'
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            u = User.objects.create_user(
                    username=form.cleaned_data.get('username'),
                    password=form.cleaned_data.get('password1'),
                    is_active = True
            )
            login(request,u)
            # TODO Display message and redirect to login
            return HttpResponseRedirect('/')
        return render(request, self.template_name, {'form': form})