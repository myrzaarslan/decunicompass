from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("unipage/<int:nid>", views.university, name="university"),
    path('api/the_universities/', views.the_universities_list, name='the_universities_list'),
    path('api/qs_universities/', views.qs_universities_list, name='qs_universities_list'),
    path('api/kz_universities/', views.kz_universities_list, name='kz_universities_list'),
    path('api/the_university/<int:nid>/', views.the_university_detail, name='the_university_detail'),
    path('api/qs_university/<int:nid>/', views.qs_university_detail, name='qs_university_detail'),
]