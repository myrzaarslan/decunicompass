from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from django.core.paginator import Paginator
from .genaicode.genai_university import get_university_info
from .models import *

# Create your views here.
def index(request):
    return render(request, "unicompass_app/index.html")

def exp(request):
    return render(request, "unicompass_app/nindex.html")

def qs_universities_list(request):
    # Get parameters from the URL
    page = int(request.GET.get('page', 0))
    items_per_page = int(request.GET.get('items_per_page', 10))
    
    # Fetch QS universities
    universities = QS_University.objects.all()

    # Pagination
    total_records = universities.count()
    total_pages = (total_records + items_per_page - 1) // items_per_page
    universities = universities[(page * items_per_page):(page * items_per_page + items_per_page)]

    # Prepare the response data
    data = list(universities.values('id', 'rank', 'title', 'overall_score', 'city', 'country'))

    response = {
        "current_page": page + 1,
        "total_pages": total_pages,
        "items_per_page": items_per_page,
        "total_records": total_records,
        "data": data
    }
    
    return JsonResponse(response)

def the_universities_list(request):
    # Get parameters from the URL
    subject_name = request.GET.get('subjectname', 'general')
    page = int(request.GET.get('page', 0))
    items_per_page = int(request.GET.get('items_per_page', 10))
    
    # Filter universities based on subjectname (if applicable)
    if subject_name != 'general':
        universities = THE_University.objects.filter(subjects_offered__icontains=subject_name)
    else:
        universities = THE_University.objects.all()

    # Pagination
    total_records = universities.count()
    total_pages = (total_records + items_per_page - 1) // items_per_page
    universities = universities[(page * items_per_page):(page * items_per_page + items_per_page)]

    # Prepare the response data
    data = list(universities.values('id', 'rank', 'name', 'scores_overall', 'nid', 'location', 'subjects_offered'))

    response = {
        "current_page": page + 1,
        "total_pages": total_pages,
        "items_per_page": items_per_page,
        "total_records": total_records,
        "data": data
    }
    
    return JsonResponse(response)

def university(request, uni):
    uni_info = get_university_info(uni)
    return render(request, "unicompass_app/unipage.html", {'uni_info': uni_info})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "unicompass_app/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "unicompass_app/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "unicompass_app/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "unicompass_app/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "unicompass_app/register.html")