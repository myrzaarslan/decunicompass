from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from django.core.paginator import Paginator
from .models import *
from django.db.models import Q
from django.core.serializers import serialize

# Create your views here.
def index(request):
    return render(request, "unicompass_app/listing.html")

# API for an individual THE university by its 'nid'
def the_university_detail(request, nid):
    university = UniUni.objects.get(the_nid=nid)

    data = {
        'title': university.the_title,
        'rank': university.the_rank,
        'rank_arts': university.the_rank_arts,
        'rank_eng': university.the_rank_eng,
        'rank_bus': university.the_rank_bus,
        'rank_law': university.the_rank_law,
        'rank_clin': university.the_rank_clin,
        'rank_life': university.the_rank_life,
        'rank_comp': university.the_rank_comp,
        'rank_phys': university.the_rank_phys,
        'rank_edu': university.the_rank_edu,
        'rank_psych': university.the_rank_psych,
        'description': university.description,
        'link': university.link,
        'img': university.img,
        'latitude': university.latitude,
        'longitude': university.longitude,
        'overall_score': university.the_overall_score,
        'location': university.the_location,
        'subjects_offered': university.the_subjects_offered,
    }
    return JsonResponse(data)

# API for an individual QS university by its 'nid'
def qs_university_detail(request, nid):
    university = UniUni.objects.get(qs_nid=nid)

    data = {
        'title': university.qs_title,
        'rank': university.qs_rank,
        'rank_arts_humanities': university.qs_rank_arts_humanities,
        'rank_arts': university.qs_rank_arts,
        'rank_linguistics': university.qs_rank_linguistics,
        'rank_music': university.qs_rank_music,
        'rank_theology': university.qs_rank_theology,
        'rank_archaeology': university.qs_rank_archaeology,
        'rank_architecture': university.qs_rank_architecture,
        'rank_art_design': university.qs_rank_art_design,
        'rank_classics': university.qs_rank_classics,
        'rank_english': university.qs_rank_english,
        'rank_history': university.qs_rank_history,
        'rank_modern_languages': university.qs_rank_modern_languages,
        'rank_philosophy': university.qs_rank_philosophy,
        'rank_eng_tech': university.qs_rank_eng_tech,
        'rank_chem_eng': university.qs_rank_chem_eng,
        'rank_civil_eng': university.qs_rank_civil_eng,
        'rank_comp_sci': university.qs_rank_comp_sci,
        'rank_data_sci': university.qs_rank_data_sci,
        'rank_elec_eng': university.qs_rank_elec_eng,
        'rank_mech_eng': university.qs_rank_mech_eng,
        'rank_nat_sci': university.qs_rank_nat_sci,
        'rank_chemistry': university.qs_rank_chemistry,
        'rank_env_sci': university.qs_rank_env_sci,
        'rank_geography': university.qs_rank_geography,
        'description': university.description,
        'link': university.link,
        'img': university.img,
        'latitude': university.latitude,
        'longitude': university.longitude,
        'overall_score': university.qs_overall_score,
        'city': university.qs_city,
        'country': university.qs_country,
    }
    return JsonResponse(data)

def qs_universities_list(request):
    subject_name = request.GET.get('subject', 'general')
    page = int(request.GET.get('page', 0))
    items_per_page = int(request.GET.get('items_per_page', 10))

    valid_subject_fields = [
        'qs_rank_arts_humanities', 'qs_rank_arts', 'qs_rank_linguistics', 'qs_rank_music', 'qs_rank_theology',
        'qs_rank_archaeology', 'qs_rank_architecture', 'qs_rank_art_design', 'qs_rank_classics', 'qs_rank_english',
        'qs_rank_history', 'qs_rank_art_history', 'qs_rank_modern_languages', 'qs_rank_performing_arts', 
        'qs_rank_philosophy', 'qs_rank_eng_tech', 'qs_rank_chem_eng', 'qs_rank_civil_eng', 'qs_rank_comp_sci', 
        'qs_rank_data_sci', 'qs_rank_elec_eng', 'qs_rank_pet_eng', 'qs_rank_mech_eng', 'qs_rank_mining_eng', 
        'qs_rank_nat_sci', 'qs_rank_chemistry', 'qs_rank_earth_marine_sci', 'qs_rank_env_sci', 'qs_rank_geography', 
        'qs_rank_geology', 'qs_rank_geophysics', 'qs_rank_materials_sci', 'qs_rank_math', 'qs_rank_physics_astronomy', 
        'qs_rank_life_sci', 'qs_rank_agriculture', 'qs_rank_anatomy', 'qs_rank_bio_sci', 'qs_rank_dentistry', 
        'qs_rank_medicine', 'qs_rank_pharmacy', 'qs_rank_nursing', 'qs_rank_psychology', 'qs_rank_vet_sci'
    ]

    # Base queryset with non-empty titles
    base_queryset = UniUni.objects.exclude(Q(qs_title__isnull=True) | Q(qs_title=''))

    if subject_name in valid_subject_fields:
        universities = base_queryset.filter(**{subject_name + '__isnull': False}).order_by(subject_name)
    else:
        universities = base_queryset.order_by('qs_rank')

    total_records = universities.count()
    total_pages = (total_records + items_per_page - 1) // items_per_page
    universities = universities[(page * items_per_page):(page * items_per_page + items_per_page)]

    data = list(universities.values('qs_nid', 'qs_rank', 'qs_title', 'qs_overall_score', 'qs_city', 'qs_country'))

    response = {
        "current_page": page + 1,
        "total_pages": total_pages,
        "items_per_page": items_per_page,
        "total_records": total_records,
        "data": data
    }

    return JsonResponse(response)

def qs_universities_by_subjects(request, subject='general'):
    page = int(request.GET.get('page', 0))
    items_per_page = int(request.GET.get('items_per_page', 10))

    valid_subject_fields = {
        # Arts & Humanities
        'arts_humanities': 'qs_rank_arts_humanities',
        'arts': 'qs_rank_arts',
        'linguistics': 'qs_rank_linguistics',
        'music': 'qs_rank_music',
        'theology': 'qs_rank_theology',
        'archaeology': 'qs_rank_archaeology',
        'architecture': 'qs_rank_architecture',
        'art_design': 'qs_rank_art_design',
        'classics': 'qs_rank_classics',
        'english': 'qs_rank_english',
        'history': 'qs_rank_history',
        'art_history': 'qs_rank_art_history',
        'modern_languages': 'qs_rank_modern_languages',
        'performing_arts': 'qs_rank_performing_arts',
        'philosophy': 'qs_rank_philosophy',

        # Engineering & Technology
        'engineering_technology': 'qs_rank_eng_tech',
        'chemical_engineering': 'qs_rank_chem_eng',
        'civil_engineering': 'qs_rank_civil_eng',
        'computer_science': 'qs_rank_comp_sci',
        'data_science': 'qs_rank_data_sci',
        'electrical_engineering': 'qs_rank_elec_eng',
        'petroleum_engineering': 'qs_rank_pet_eng',
        'mechanical_engineering': 'qs_rank_mech_eng',
        'mining_engineering': 'qs_rank_mining_eng',

        # Natural Sciences
        'natural_sciences': 'qs_rank_nat_sci',
        'chemistry': 'qs_rank_chemistry',
        'earth_marine_sciences': 'qs_rank_earth_marine_sci',
        'environmental_sciences': 'qs_rank_env_sci',
        'geography': 'qs_rank_geography',
        'geology': 'qs_rank_geology',
        'geophysics': 'qs_rank_geophysics',
        'materials_science': 'qs_rank_materials_sci',
        'mathematics': 'qs_rank_math',
        'physics_astronomy': 'qs_rank_physics_astronomy',

        # Life Sciences & Medicine
        'life_sciences_medicine': 'qs_rank_life_sci',
        'agriculture': 'qs_rank_agriculture',
        'anatomy': 'qs_rank_anatomy',
        'biological_sciences': 'qs_rank_bio_sci',
        'dentistry': 'qs_rank_dentistry',
        'medicine': 'qs_rank_medicine',
        'pharmacy': 'qs_rank_pharmacy',
        'nursing': 'qs_rank_nursing',
        'psychology': 'qs_rank_psychology',
        'veterinary_science': 'qs_rank_vet_sci',

        # Social Sciences & Management
        'social_sciences_management': 'qs_rank_social_sci_management',
        'accounting_finance': 'qs_rank_accounting_finance',
        'anthropology': 'qs_rank_anthropology',
        'business_management': 'qs_rank_business_management',
        'communication_media': 'qs_rank_comm_media',
        'development_studies': 'qs_rank_dev_studies',
        'economics_econometrics': 'qs_rank_economics_econometrics',
        'education': 'qs_rank_education',
        'hospitality_leisure': 'qs_rank_hospitality_leisure',
        'law': 'qs_rank_law',
        'politics_international_studies': 'qs_rank_politics_international_studies',
        'social_policy_admin': 'qs_rank_social_policy_admin',
        'sociology': 'qs_rank_sociology',
        'sports_related': 'qs_rank_sports_related',

        # Additional Subjects (if needed)
        # Add more fields as necessary
    }


    # Base queryset with non-empty titles
    base_queryset = UniUni.objects.exclude(Q(qs_title__isnull=True) | Q(qs_title=''))

    if subject in valid_subject_fields:
        ranking_field = valid_subject_fields[subject]
        universities = base_queryset.filter(**{ranking_field + '__isnull': False}).order_by(ranking_field)
    else:
        universities = base_queryset.order_by('qs_rank')

    total_records = universities.count()
    total_pages = (total_records + items_per_page - 1) // items_per_page
    universities = universities[(page * items_per_page):(page * items_per_page + items_per_page)]

    data = list(universities.values('qs_nid', 'qs_rank', 'qs_title', 'qs_overall_score', 'qs_city', 'qs_country'))

    response = {
        "current_page": page + 1,
        "total_pages": total_pages,
        "items_per_page": items_per_page,
        "total_records": total_records,
        "data": data
    }

    return JsonResponse(response)

def the_universities_list(request):
    subject_name = request.GET.get('subject', 'general')
    page = int(request.GET.get('page', 0))
    items_per_page = int(request.GET.get('items_per_page', 10))

    valid_subject_fields = [
        'the_rank_arts', 'the_rank_bus', 'the_rank_clin', 'the_rank_comp', 'the_rank_edu', 'the_rank_eng', 
        'the_rank_law', 'the_rank_life', 'the_rank_phys', 'the_rank_psych'
    ]

    # Base queryset with non-empty titles
    base_queryset = UniUni.objects.exclude(Q(the_title__isnull=True) | Q(the_title=''))

    if subject_name in valid_subject_fields:
        universities = base_queryset.filter(**{subject_name + '__isnull': False}).order_by(subject_name)
    else:
        universities = base_queryset.order_by('the_rank')

    total_records = universities.count()
    total_pages = (total_records + items_per_page - 1) // items_per_page
    universities = universities[(page * items_per_page):(page * items_per_page + items_per_page)]

    data = list(universities.values('the_nid', 'the_rank', 'the_title', 'the_overall_score', 'the_location', 'the_subjects_offered'))

    response = {
        "current_page": page + 1,
        "total_pages": total_pages,
        "items_per_page": items_per_page,
        "total_records": total_records,
        "data": data
    }

    return JsonResponse(response)

def the_universities_by_subjects(request, subject='general'):
    page = int(request.GET.get('page', 0))
    items_per_page = int(request.GET.get('items_per_page', 10))

    valid_subject_fields = {
        'arts': 'the_rank_arts',
        'business': 'the_rank_bus',
        'clinical': 'the_rank_clin',
        'computer': 'the_rank_comp',
        'education': 'the_rank_edu',
        'engineering': 'the_rank_eng',
        'law': 'the_rank_law',
        'life_sciences': 'the_rank_life',
        'physical_sciences': 'the_rank_phys',
        'psychology': 'the_rank_psych'
    }

    # Base queryset with non-empty titles
    base_queryset = UniUni.objects.exclude(Q(the_title__isnull=True) | Q(the_title=''))

    if subject in valid_subject_fields:
        ranking_field = valid_subject_fields[subject]
        universities = base_queryset.filter(**{ranking_field + '__isnull': False}).order_by(ranking_field)
    else:
        universities = base_queryset.order_by('the_rank')

    total_records = universities.count()
    total_pages = (total_records + items_per_page - 1) // items_per_page
    universities = universities[(page * items_per_page):(page * items_per_page + items_per_page)]

    data = list(universities.values('the_nid', 'the_rank', 'the_title', 'the_overall_score', 'the_location', 'the_subjects_offered'))

    response = {
        "current_page": page + 1,
        "total_pages": total_pages,
        "items_per_page": items_per_page,
        "total_records": total_records,
        "data": data
    }

    return JsonResponse(response)

def all_university_details(request):
    university_id = request.GET.get('id')
    
    if university_id:
        try:
            university = UniUni.objects.get(id=university_id)
            data = serialize('python', [university])[0]['fields']
            data['id'] = university.id  # Add the id field
            return JsonResponse(data)
        except UniUni.DoesNotExist:
            return JsonResponse({"error": "University not found"}, status=404)
    else:
        page = int(request.GET.get('page', 0))
        items_per_page = int(request.GET.get('items_per_page', 10))

        universities = UniUni.objects.all()
        total_records = universities.count()
        total_pages = (total_records + items_per_page - 1) // items_per_page
        universities = universities[(page * items_per_page):(page * items_per_page + items_per_page)]

        data = []
        for university in universities:
            uni_data = serialize('python', [university])[0]['fields']
            uni_data['id'] = university.id  # Add the id field
            data.append(uni_data)

        response = {
            "current_page": page + 1,
            "total_pages": total_pages,
            "items_per_page": items_per_page,
            "total_records": total_records,
            "data": data
        }

        return JsonResponse(response)

def universities_by_subject(request, subject):
    page = int(request.GET.get('page', 0))
    items_per_page = int(request.GET.get('items_per_page', 10))

    valid_subject_fields = {
    # THE subject fields
    'the_arts': 'the_rank_arts',
    'the_business': 'the_rank_bus',
    'the_clinical': 'the_rank_clin',
    'the_computer': 'the_rank_comp',
    'the_education': 'the_rank_edu',
    'the_engineering': 'the_rank_eng',
    'the_law': 'the_rank_law',
    'the_life_sciences': 'the_rank_life',
    'the_physical_sciences': 'the_rank_phys',
    'the_psychology': 'the_rank_psych',
    
    # QS subject fields
    'qs_arts_humanities': 'qs_rank_arts_humanities',
    'qs_engineering_tech': 'qs_rank_eng_tech',
    'qs_life_sciences_medicine': 'qs_rank_life_sci',
    'qs_natural_sciences': 'qs_rank_nat_sci',
    
    # Arts & Humanities
    'qs_arts': 'qs_rank_arts',
    'qs_linguistics': 'qs_rank_linguistics',
    'qs_music': 'qs_rank_music',
    'qs_theology': 'qs_rank_theology',
    'qs_archaeology': 'qs_rank_archaeology',
    'qs_architecture': 'qs_rank_architecture',
    'qs_art_design': 'qs_rank_art_design',
    'qs_classics': 'qs_rank_classics',
    'qs_english': 'qs_rank_english',
    'qs_history': 'qs_rank_history',
    'qs_art_history': 'qs_rank_art_history',
    'qs_modern_languages': 'qs_rank_modern_languages',
    'qs_performing_arts': 'qs_rank_performing_arts',
    'qs_philosophy': 'qs_rank_philosophy',

    # Engineering & Technology
    'qs_chemical_engineering': 'qs_rank_chem_eng',
    'qs_civil_engineering': 'qs_rank_civil_eng',
    'qs_computer_science': 'qs_rank_comp_sci',
    'qs_data_science': 'qs_rank_data_sci',
    'qs_electrical_engineering': 'qs_rank_elec_eng',
    'qs_petroleum_engineering': 'qs_rank_pet_eng',
    'qs_mechanical_engineering': 'qs_rank_mech_eng',
    'qs_mining_engineering': 'qs_rank_mining_eng',

    # Natural Sciences
    'qs_chemistry': 'qs_rank_chemistry',
    'qs_earth_marine_sciences': 'qs_rank_earth_marine_sci',
    'qs_environmental_sciences': 'qs_rank_env_sci',
    'qs_geography': 'qs_rank_geography',
    'qs_geology': 'qs_rank_geology',
    'qs_geophysics': 'qs_rank_geophysics',
    'qs_materials_science': 'qs_rank_materials_sci',
    'qs_mathematics': 'qs_rank_math',
    'qs_physics_astronomy': 'qs_rank_physics_astronomy',

    # Life Sciences & Medicine
    'qs_agriculture': 'qs_rank_agriculture',
    'qs_anatomy': 'qs_rank_anatomy',
    'qs_biological_sciences': 'qs_rank_bio_sci',
    'qs_dentistry': 'qs_rank_dentistry',
    'qs_medicine': 'qs_rank_medicine',
    'qs_pharmacy': 'qs_rank_pharmacy',
    'qs_nursing': 'qs_rank_nursing',
    'qs_psychology': 'qs_rank_psychology',
    'qs_veterinary_science': 'qs_rank_vet_sci',

    # Social Sciences & Management
    'qs_accounting_finance': 'qs_rank_accounting_finance',
    'qs_anthropology': 'qs_rank_anthropology',
    'qs_business_management': 'qs_rank_business_management',
    'qs_communication_media': 'qs_rank_comm_media',
    'qs_development_studies': 'qs_rank_dev_studies',
    'qs_economics_econometrics': 'qs_rank_economics_econometrics',
    'qs_education': 'qs_rank_education',
    'qs_hospitality_leisure': 'qs_rank_hospitality_leisure',
    'qs_law': 'qs_rank_law',
    'qs_politics_international_studies': 'qs_rank_politics_international_studies',
    'qs_social_policy_admin': 'qs_rank_social_policy_admin',
    'qs_sociology': 'qs_rank_sociology',
    'qs_sports_related': 'qs_rank_sports_related',
    }

    if subject not in valid_subject_fields:
        return JsonResponse({"error": "Invalid subject"}, status=400)

    ranking_field = valid_subject_fields[subject]
    ranking_system = 'the' if subject.startswith('the_') else 'qs'

    universities = UniUni.objects.filter(**{ranking_field + '__isnull': False}).order_by(ranking_field)

    total_records = universities.count()
    total_pages = (total_records + items_per_page - 1) // items_per_page
    universities = universities[(page * items_per_page):(page * items_per_page + items_per_page)]

    data = []
    for uni in universities:
        uni_data = {
            'id': uni.id,
            'title': uni.the_title if ranking_system == 'the' else uni.qs_title,
            'rank': getattr(uni, ranking_field),
            'overall_score': uni.the_overall_score if ranking_system == 'the' else uni.qs_overall_score,
        }
        if ranking_system == 'the':
            uni_data.update({
                'location': uni.the_location,
                'subjects_offered': uni.the_subjects_offered,
            })
        else:
            uni_data.update({
                'city': uni.qs_city,
                'country': uni.qs_country,
            })
        data.append(uni_data)

    response = {
        "current_page": page + 1,
        "total_pages": total_pages,
        "items_per_page": items_per_page,
        "total_records": total_records,
        "data": data
    }

    return JsonResponse(response)

def kz_universities_list(request):
    page = int(request.GET.get('page', 0))
    items_per_page = int(request.GET.get('items_per_page', 10))

    # Filter universities with non-null and non-empty kz_title
    universities = UniUni.objects.exclude(Q(kz_title__isnull=True) | Q(kz_title=''))
    
    total_records = universities.count()
    total_pages = (total_records + items_per_page - 1) // items_per_page
    universities = universities[(page * items_per_page):(page * items_per_page + items_per_page)]

    data = []
    for university in universities:
        uni_data = serialize('python', [university])[0]['fields']
        uni_data['id'] = university.id  # Add the id field
        data.append(uni_data)

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