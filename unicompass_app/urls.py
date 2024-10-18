from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("unipage/<int:id>", views.university, name="university"),
    path('api/chat/', views.chat_view, name='chat'),
    path('api/uni/kz', views.kz_universities_list, name='kz_universities_list'),
    path('api/uni/the/<int:id>/', views.the_university_detail, name='the_university_detail'),
    path('api/uni/qs/<int:id>/', views.qs_university_detail, name='qs_university_detail'),
    path('api/uni/the/<str:subject>/', views.the_universities_by_subjects, name='the_universities_by_subject'),
    path('api/uni/qs/<str:subject>/', views.qs_universities_by_subjects, name='qs_universities_by_subjects'),
    path('api/uni/the/', views.the_universities_list, name='the_universities_list'),
    path('api/uni/qs/', views.qs_universities_list, name='qs_universities_list'),
    path('api/uni/', views.all_university_details, name='all_university_details'),
    path('api/uni/<str:subject>/', views.universities_by_subject, name='universities_by_subject'),
]