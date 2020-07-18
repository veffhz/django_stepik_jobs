from django.urls import path
from django.contrib.auth.views import LogoutView

from vacancies.models import Skill

from vacancies.views import (
    ResumeUpdateView, ResumeCreateView, ProfileView,
    MyCompanyUpdateView, MyCompanyCreateView, SkillAutoComplete,
    MainView, VacancyListView, CompanyListView, ApplicationView,
    MyCompanyVacancyListView, MyCompanyVacancyUpdateView, MyCompanyVacancyCreateView,
    CompanyDetailView, VacancyDetailView, SpecialtyView, AboutView, SearchVacanciesView,
)

from vacancies.views import (
    custom_handler404,
    custom_handler500,
    custom_handler403,
    CustomLoginView, RegisterView
)

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('about', AboutView.as_view(), name='about'),

    path('companies/', CompanyListView.as_view(), name='companies'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company'),

    path('vacancies/', VacancyListView.as_view(), name='vacancies'),
    path('vacancies/cat/<str:specialty_code>/', SpecialtyView.as_view(), name='vacancies-category'),
    path('vacancies/<int:pk>/', VacancyDetailView.as_view(), name='vacancy'),
    path('vacancies/<int:vacancy_id>/send/', ApplicationView.as_view(), name='vacancy-send'),

    path('mycompany/', MyCompanyUpdateView.as_view(), name='my-company'), # noqa
    path('mycompany/create/', MyCompanyCreateView.as_view(), name='create-company'), # noqa

    path('mycompany/vacancies/', MyCompanyVacancyListView.as_view(), name='my-vacancies'), # noqa
    path('mycompany/vacancies/<int:pk>/', MyCompanyVacancyUpdateView.as_view(), name='my-vacancy'), # noqa
    path('mycompany/vacancies/create/', MyCompanyVacancyCreateView.as_view(), name='create-vacancy'), # noqa

    path('myresume/', ResumeUpdateView.as_view(), name='resume'), # noqa
    path('myresume/create/', ResumeCreateView.as_view(), name='create-resume'), # noqa

    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('search/', SearchVacanciesView.as_view(), name='search'),

    path('skill-autocomplete/', SkillAutoComplete.as_view(
        model=Skill, create_field='title'), name='skill-autocomplete')
]

handler403 = custom_handler403
handler404 = custom_handler404
handler500 = custom_handler500
