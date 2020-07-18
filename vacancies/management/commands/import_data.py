from random import randint

from django.conf import settings
from django.core.management.base import BaseCommand

from vacancies.models import Company, Specialty, Vacancy, Skill, CustomUser
from vacancies.data.vacancies_data import jobs, companies, specialties


class Command(BaseCommand):
    help = 'Master data import'

    def handle(self, *args, **options):
        run()


def run():

    cache = {
        'companies': {},
        'specialties': {},
    }

    for _specialty in specialties:
        picture = _specialty.get('logo', '')

        if picture:
            picture = f'{settings.MEDIA_SPECIALITY_IMAGE_DIR}/{picture}'
        else:
            picture = f'{settings.MEDIA_SPECIALITY_IMAGE_DIR}/{settings.NO_LOGO_PIC}'

        specialty = Specialty.objects.create(
            code=_specialty['code'], title=_specialty['title'],
            picture=picture
        )
        cache['specialties'][specialty.code] = specialty

    for company_no, _company in enumerate(companies):
        logo = _company.get('logo', '')

        if logo:
            logo = f'{settings.MEDIA_COMPANY_IMAGE_DIR}/{logo}'
        else:
            logo = f'{settings.MEDIA_COMPANY_IMAGE_DIR}/no_logo.png'

        company = Company.objects.create(
            name=_company['title'], location=_company['location'],
            employee_count=randint(1, 10), logo=logo,
            description=_company.get('description', ''),
            owner=create_user(company_no)
        )
        cache['companies'][company.name] = company

    for job in jobs:
        vacancy = Vacancy(
            title=job['title'],
            published_at=job['posted'],
            salary_min=job.get('salary_from'),
            salary_max=job.get('salary_to'),
            description=job['desc'],
            specialty=cache['specialties'][job['cat']],
            company=cache['companies'][job['company']],
            is_remote=job.get('is_remote', False),
        )
        vacancy.save()

        for _skill in job.get('skills', []):
            skill, _ = Skill.objects.get_or_create(title=_skill)
            vacancy.skills.add(skill)
            vacancy.save()


def create_user(company_no):
    return CustomUser.objects.create_user(
        username=f'test_user_{company_no}',
        password=f'Password{company_no}',
        is_company=True,
    )
