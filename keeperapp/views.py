from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):

    return redirect(user_home)

@login_required(login_url='/user/sign-in')
def user_home(request):

    return render(request, 'user/home.html')
