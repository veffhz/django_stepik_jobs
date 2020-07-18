from django import forms
from dal import autocomplete
from django.forms import ValidationError
from phonenumbers import NumberParseException
from phonenumbers import parse, is_valid_number
from cached_modelforms import CachedModelChoiceField
from django.contrib.auth.forms import UserCreationForm

from vacancies.models import (
    Company, Specialty, Skill, Vacancy,
    Resume, CustomUser, Application,
)

default_attrs = {
    'class': 'form-control'
}


def validate_phone_number(value):
    try:
        phone = parse(value, 'RU')
        if not is_valid_number(phone):
            raise NumberParseException(phone, '')
    except NumberParseException:
        raise ValidationError(f'{value} неверный формат номера!')


class ApplicationForm(forms.ModelForm):
    written_username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs=default_attrs),
        label='Вас зовут'
    )

    written_phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'type': 'tel',
            'class': 'form-control',
        }),
        label='Ваш телефон',
        validators=[validate_phone_number]
    )

    class Meta:
        model = Application
        fields = (
            'written_username',
            'written_phone',
            'written_cover_letter'
        )
        labels = {
            'written_cover_letter': 'Сопроводительное письмо',
        }
        widgets = {
            'written_cover_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '8'
            }),
        }


class CompanyForm(forms.ModelForm):
    logo = forms.ImageField(
        required=False,
        error_messages={'invalid': "Image files only"},
        widget=forms.FileInput(),
        label='Логотип'
    )

    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs=default_attrs),
        label='Название компании'
    )

    location = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs=default_attrs
    ), label='География')

    class Meta:
        model = Company
        fields = ('name', 'logo', 'employee_count', 'location', 'description')
        labels = {
            'employee_count': 'Количество человек в компании',
            'description': 'Информация о компании',
        }
        widgets = {
            'employee_count': forms.NumberInput(attrs={'id': 'companyTeam', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '5'
            }),
        }


class VacancyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VacancyForm, self).__init__(*args, **kwargs)
        self.fields['specialty'].objects = Specialty.objects.all()

    title = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs=default_attrs
    ), label='Название вакансии')

    salary_min = forms.IntegerField(required=False, widget=forms.NumberInput(
        attrs=default_attrs
    ), label='Зарплата от')

    salary_max = forms.IntegerField(required=False, widget=forms.NumberInput(
        attrs=default_attrs
    ), label='Зарплата до')

    specialty = CachedModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'custom-select mr-sm-2'
        }),
        label='Специализация'
    )

    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(
            url='skill-autocomplete',
            attrs={
                'data-minimum-input-length': 1
            }),
        label='Требуемые навыки'
    )

    class Meta:
        model = Vacancy
        fields = (
            'title',
            'specialty',
            'salary_min',
            'salary_max',
            'description',
            'is_remote',
            'skills',
        )
        labels = {
            'is_remote': 'Удаленно',
            'description': 'Описание вакансии',
        }
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '13'
            }),
        }


class ResumeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ResumeForm, self).__init__(*args, **kwargs)
        self.fields['specialty'].objects = Specialty.objects.all()

    name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs=default_attrs
    ), label='Имя')

    surname = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs=default_attrs
    ), label='Фамилия')

    salary = forms.IntegerField(required=False, widget=forms.NumberInput(
        attrs=default_attrs
    ), label='Ожидаемое вознаграждение')

    specialty = CachedModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'custom-select mr-sm-2'
        }),
        label='Специализация'
    )

    portfolio = forms.CharField(max_length=300, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'http://anylink.github.io'
        }
    ), label='Ссылка на портфолио')

    class Meta:
        model = Resume
        fields = (
            'name',
            'surname',
            'salary',
            'experience',
            'portfolio',
            'institution',
            'status',
            'grade',
            'education',
            'specialty'
        )
        labels = {
            'education': 'Образование',
            'grade': 'Квалификация',
            'status': 'Готовность к работе',
            'institution': 'Учебное заведение',
            'experience': 'Опыт работы',
        }
        widgets = {
            'education': forms.Select(attrs={'class': 'custom-select mr-sm-2'}),
            'grade': forms.Select(attrs={'class': 'custom-select mr-sm-2'}),
            'status': forms.Select(attrs={'class': 'custom-select mr-sm-2'}),

            'experience': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '4'
            }),
            'institution': forms.Textarea(attrs={
                'class': 'form-control text-uppercase',
                'rows': '4'
            }),
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username', 'first_name', 'last_name',
            'password1', 'password2', 'is_company'
        )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'first_name', 'last_name', 'is_company'
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_company': forms.CheckboxInput(attrs={'class': 'form-control-lg form-check-input'}),
        }
