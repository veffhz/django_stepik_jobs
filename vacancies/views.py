from dal import autocomplete
from django.conf import settings
from django.contrib import messages
from django.db.models import Count, Q
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from vacancies.forms import (
    ApplicationForm, CompanyForm, VacancyForm,
    ResumeForm, CustomUserCreationForm, UserProfileForm
)
from vacancies.models import (
    Specialty, Company, Vacancy, Skill, Resume
)


class MainView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.annotate(vacancies_count=Count('vacancies'))
        context['companies'] = Company.objects.annotate(vacancies_count=Count('vacancies'))
        context['example_queries'] = ['Python', 'Flask', 'Django', 'Kafka', 'MySql']
        return context


class VacancyListView(ListView):
    template_name = 'vacancies.html'
    context_object_name = 'vacancies'
    queryset = (
        Vacancy.objects.all()
        .select_related('company')
        .prefetch_related('skills')
    )


class CompanyListView(ListView):
    template_name = 'companies.html'
    queryset = Company.objects.all()
    context_object_name = 'companies'


class CompanyDetailView(DetailView):
    template_name = 'company.html'
    model = Company
    queryset = (
        Company.objects.prefetch_related(
            'vacancies', 'vacancies__skills'
        )
    )


class SpecialtyView(TemplateView):
    template_name = 'vacancies.html'

    def get_context_data(self, **kwargs):
        context = super(SpecialtyView, self).get_context_data(**kwargs)
        specialty_code = kwargs['specialty_code']
        query = Specialty.objects.prefetch_related(
            'vacancies', 'vacancies__skills', 'vacancies__company'
        )
        specialty = get_object_or_404(query, code=specialty_code)
        context['vacancies'] = specialty.vacancies.all()
        context['specialty'] = specialty
        return context


class VacancyDetailView(FormMixin, DetailView):
    template_name = 'vacancy.html'
    model = Vacancy
    form_class = ApplicationForm
    queryset = (
        Vacancy.objects.select_related('company')
    )

    def get_success_url(self):
        return reverse('vacancy-send', args=(self.object.id,))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # noqa
        form = ApplicationForm(request.POST or None)

        if form.is_valid():
            application = form.save(commit=False)

            application.vacancy = self.object

            if request.user.is_authenticated:
                application.user = self.request.user

            application.save()
            return self.form_valid(form)

        return self.form_invalid(form)


class ApplicationView(View):
    def get(self, request, vacancy_id, *args, **kwargs):
        previous_page = request.META.get('HTTP_REFERER')

        vacancy_url = reverse('vacancy', kwargs={'pk': vacancy_id})

        # Проверяем, что перешли со страницы вакансии
        if not previous_page or vacancy_url not in previous_page:
            return HttpResponseRedirect(reverse('vacancy', args=[vacancy_id]))

        context = {'vacancy_id': vacancy_id}
        return render(request, 'sent.html', context=context)


class MyCompanyUpdateView(LoginRequiredMixin, UserPassesTestMixin,
                          SuccessMessageMixin, UpdateView):
    model = Company
    template_name = 'authorized/company-edit.html'
    form_class = CompanyForm
    success_url = reverse_lazy('my-company')
    success_message = 'Информация о компании обновлена'

    def test_func(self):
        return self.request.user.is_company

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()  # noqa
        if not self.object:
            return HttpResponseRedirect(reverse('create-company'))
        return self.render_to_response(self.get_context_data())

    def get_object(self, **kwargs):
        return Company.objects.filter(owner=self.request.user).first()


class MyCompanyCreateView(LoginRequiredMixin, UserPassesTestMixin,
                          SuccessMessageMixin, CreateView):
    model = Company
    template_name = 'authorized/company-create.html'
    form_class = CompanyForm
    success_url = reverse_lazy('my-company')
    success_message = 'Компания создана'

    def test_func(self):
        return self.request.user.is_company

    def get(self, request, *args, **kwargs):
        self.object = None  # noqa
        if hasattr(self.request.user, 'company'):
            return HttpResponseRedirect(reverse('my-company'))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        if not form.instance.logo:
            form.instance.logo = f'{settings.MEDIA_COMPANY_IMAGE_DIR}/{settings.NO_LOGO_PIC}'
        return super(MyCompanyCreateView, self).form_valid(form)


class MyCompanyVacancyListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "authorized/vacancy-list.html"
    context_object_name = 'vacancies'

    def test_func(self):
        return self.request.user.is_company

    def get(self, request, *args, **kwargs):
        if not hasattr(self.request.user, 'company'):
            return HttpResponseRedirect(reverse('create-company'))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        qs = (user.company.vacancies
              .prefetch_related('applications'))
        if not qs:
            messages.info(
                self.request,
                'У Вас пока нет вакансий, но Вы можете создать первую!',
            )
        return qs


class MyCompanyVacancyUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Vacancy
    template_name = 'authorized/vacancy-edit.html'
    form_class = VacancyForm
    success_message = 'Информация о вакансии обновлена'

    def get_object(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)
        query = Vacancy.objects.select_related('company', 'company__owner')
        vacancy = get_object_or_404(query, pk=pk)

        if vacancy.company.owner != self.request.user:
            raise PermissionDenied("Доступ к вакансии запрещен")

        return vacancy

    def get_success_url(self, **kwargs):
        return reverse_lazy('my-vacancy', args=(self.object.id,))


class MyCompanyVacancyCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Vacancy
    template_name = 'authorized/vacancy-create.html'
    form_class = VacancyForm
    success_message = 'Вакансия создана'

    def get_success_url(self, **kwargs):
        return reverse_lazy('my-vacancy', args=(self.object.id,))

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        return super(MyCompanyVacancyCreateView, self).form_valid(form)


class SkillAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Skill.objects.none()

        qs = Skill.objects.all()

        if self.q:
            qs = qs.filter(title__istartswith=self.q)

        return qs

    def has_add_permission(self, request):
        return True


class ResumeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Resume
    template_name = 'authorized/resume-edit.html'
    form_class = ResumeForm
    success_url = reverse_lazy('resume')
    success_message = 'Ваше резюме обновлено'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()  # noqa
        if not self.object:
            return HttpResponseRedirect(reverse('create-resume'))
        return self.render_to_response(self.get_context_data())

    def get_object(self, **kwargs):
        return Resume.objects.filter(user=self.request.user).first()


class ResumeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Resume
    template_name = 'authorized/resume-create.html'
    form_class = ResumeForm
    success_url = reverse_lazy('resume')
    success_message = 'Ваше резюме создано'

    def get(self, request, *args, **kwargs):
        self.object = None  # noqa
        if hasattr(self.request.user, 'resume'):
            return HttpResponseRedirect(reverse('resume'))
        return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ResumeCreateView, self).form_valid(form)


class SearchVacanciesView(ListView):
    template_name = 'search.html'
    context_object_name = 'vacancies'

    def get_context_data(self, **kwargs):
        context = super(SearchVacanciesView, self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')
        return context

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        if query:
            qs = (
                Vacancy.objects
                .select_related('company')
                .prefetch_related('skills')
                .filter(Q(title__icontains=query) | Q(skills__title__icontains=query))
                .distinct()
            )
            return qs
        else:
            return Vacancy.objects.none()


class ProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = UserProfileForm
    success_url = reverse_lazy('profile')
    template_name = 'authorized/profile.html'
    success_message = 'Профиль обновлен'

    def get_object(self, queryset=None):
        return self.request.user


class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'register.html'

    def form_valid(self, form):
        valid = super(RegisterView, self).form_valid(form)

        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )

        login(self.request, user)
        return valid


class AboutView(TemplateView):
    template_name = 'about.html'


def custom_handler403(request, exception):
    return render(request, '403.html')


def custom_handler404(request, exception):
    return render(request, '404.html')


def custom_handler500(request):
    return render(request, '500.html')
