from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from django.core.paginator import Paginator
from .models import *

# Create your views here.
def index(request):
    return render(request, "unicompass_app/listing.html")

def the_university_detail(request, nid):
    university = THE_University.objects.get(nid=nid)

    data = {
        'title': university.title,
        'rank': university.rank,
        'rank_arts': university.rank_arts,
        'rank_eng': university.rank_eng,
        'rank_bus': university.rank_bus,
        'rank_law': university.rank_law,
        'rank_clin': university.rank_clin,
        'rank_life': university.rank_life,
        'rank_comp': university.rank_comp,
        'rank_phys': university.rank_phys,
        'rank_edu': university.rank_edu,
        'rank_psych': university.rank_psych,
        'description': university.description,
        'link': university.link,
        'img': university.img,
        'latitude': university.latitude,
        'longitude': university.longitude,
        'overall_score': university.overall_score,
        'location': university.location,
        'subjects_offered': university.subjects_offered,
    }
    return JsonResponse(data)

# API for an individual QS university by its 'nid' or 'id'
def qs_university_detail(request, nid):
    university = QS_University.objects.get(nid=nid)

    data = {
        'title': university.title,
        'rank': university.rank,
        'rank_arts_humanities': university.rank_arts_humanities,
        'rank_arts': university.rank_arts,
        'rank_linguistics': university.rank_linguistics,
        'rank_music': university.rank_music,
        'rank_theology': university.rank_theology,
        'rank_archaeology': university.rank_archaeology,
        'rank_architecture': university.rank_architecture,
        'rank_art_design': university.rank_art_design,
        'rank_classics': university.rank_classics,
        'rank_english': university.rank_english,
        'rank_history': university.rank_history,
        'rank_modern_languages': university.rank_modern_languages,
        'rank_philosophy': university.rank_philosophy,
        'rank_eng_tech': university.rank_eng_tech,
        'rank_chem_eng': university.rank_chem_eng,
        'rank_civil_eng': university.rank_civil_eng,
        'rank_comp_sci': university.rank_comp_sci,
        'rank_data_sci': university.rank_data_sci,
        'rank_elec_eng': university.rank_elec_eng,
        'rank_mech_eng': university.rank_mech_eng,
        'rank_nat_sci': university.rank_nat_sci,
        'rank_chemistry': university.rank_chemistry,
        'rank_env_sci': university.rank_env_sci,
        'rank_geography': university.rank_geography,
        'description': university.description,
        'link': university.link,
        'img': university.img,
        'latitude': university.latitude,
        'longitude': university.longitude,
        'overall_score': university.overall_score,
        'city': university.city,
        'country': university.country,
    }
    return JsonResponse(data)

def qs_universities_list(request):
    # Get parameters from the URL
    subject_name = request.GET.get('subject', 'general')  # Default to 'general' if no subject is provided
    page = int(request.GET.get('page', 0))
    items_per_page = int(request.GET.get('items_per_page', 10))

    # List of all valid subject fields in the QS_University model
    valid_subject_fields = [
        'rank_arts_humanities', 'rank_arts', 'rank_linguistics', 'rank_music', 'rank_theology',
        'rank_archaeology', 'rank_architecture', 'rank_art_design', 'rank_classics', 'rank_english',
        'rank_history', 'rank_art_history', 'rank_modern_languages', 'rank_performing_arts', 
        'rank_philosophy', 'rank_eng_tech', 'rank_chem_eng', 'rank_civil_eng', 'rank_comp_sci', 
        'rank_data_sci', 'rank_elec_eng', 'rank_pet_eng', 'rank_mech_eng', 'rank_mining_eng', 
        'rank_nat_sci', 'rank_chemistry', 'rank_earth_marine_sci', 'rank_env_sci', 'rank_geography', 
        'rank_geology', 'rank_geophysics', 'rank_materials_sci', 'rank_math', 'rank_physics_astronomy', 
        'rank_life_sci', 'rank_agriculture', 'rank_anatomy', 'rank_bio_sci', 'rank_dentistry', 
        'rank_medicine', 'rank_pharmacy', 'rank_nursing', 'rank_psychology', 'rank_vet_sci'
    ]

    # Validate the subject_name and filter universities
    if subject_name in valid_subject_fields:
        # Filter universities that have a ranking for the specified subject
        universities = QS_University.objects.filter(**{subject_name + '__isnull': False}).order_by(subject_name)
    else:
        # Default to all universities if subject is 'general' or invalid
        universities = QS_University.objects.all().order_by('rank')

    # Pagination
    total_records = universities.count()
    total_pages = (total_records + items_per_page - 1) // items_per_page
    universities = universities[(page * items_per_page):(page * items_per_page + items_per_page)]

    # Prepare the response data
    data = list(universities.values('id', 'nid', 'link_id', 'rank', 'title', 'overall_score', 'city', 'country'))

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
    subject_name = request.GET.get('subject', 'general')  # Default to 'general' if no subject is provided
    page = int(request.GET.get('page', 0))
    items_per_page = int(request.GET.get('items_per_page', 10))

    # List of all valid subject fields in the THE_University model
    valid_subject_fields = [
        'rank_arts', 'rank_bus', 'rank_clin', 'rank_comp', 'rank_edu', 'rank_eng', 
        'rank_law', 'rank_life', 'rank_phys', 'rank_psych'
    ]

    # Filter universities based on the subject
    if subject_name != 'general':
        universities = THE_University.objects.filter(**{subject_name + '__isnull': False}).order_by(subject_name)
    else:
        universities = THE_University.objects.all()

    # Pagination
    total_records = universities.count()
    total_pages = (total_records + items_per_page - 1) // items_per_page
    universities = universities[(page * items_per_page):(page * items_per_page + items_per_page)]

    # Prepare the response data
    data = list(universities.values('id', 'nid', 'link_id', 'rank', 'title', 'overall_score', 'nid', 'location', 'subjects_offered'))

    response = {
        "current_page": page + 1,
        "total_pages": total_pages,
        "items_per_page": items_per_page,
        "total_records": total_records,
        "data": data
    }

    return JsonResponse(response)

def kz_universities_list(request):
    # Get pagination parameters from the URL
    page = int(request.GET.get('page', 0))
    items_per_page = int(request.GET.get('items_per_page', 10))

    # Get all universities
    universities = University.objects.all().order_by('title')

    # Pagination logic
    total_records = universities.count()
    total_pages = (total_records + items_per_page - 1) // items_per_page
    universities = universities[(page * items_per_page):(page * items_per_page + items_per_page)]

    # Prepare the response data
    data = list(universities.values('id', 'title'))

    response = {
        "current_page": page + 1,
        "total_pages": total_pages,
        "items_per_page": items_per_page,
        "total_records": total_records,
        "data": data
    }

    return JsonResponse(response)

def university(request, nid):
    # Check if university exists in either QS or THE models by link_id or nid

    # First check based on link_id
    qs_uni = QS_University.objects.filter(link_id=nid).first()
    the_uni = THE_University.objects.filter(link_id=nid).first()

    if not qs_uni and not the_uni:
        # If no match by link_id, check by nid
        qs_uni = QS_University.objects.filter(nid=nid).first()
        the_uni = THE_University.objects.filter(nid=nid).first()

    # Determine which university to use
    if qs_uni:
        uni = qs_uni
        the_rank = THE_University.objects.filter(link_id=qs_uni.link_id).first().rank if qs_uni.link_id else None
    elif the_uni:
        uni = the_uni
        the_rank = the_uni.rank
    else:
        # If neither QS nor THE university exists, return a 404 page
        return render(request, "404.html", {"message": "University not found"})

    # Render the university page with the details
    return render(request, "unicompass_app/unipage.html", {
        "uni": uni,
        "the_rank": the_rank,
    })

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