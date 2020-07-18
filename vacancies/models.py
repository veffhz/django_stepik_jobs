from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Company(models.Model):
    name = models.CharField('Название', max_length=50, unique=True)
    location = models.CharField('Город', max_length=30)
    description = models.TextField('Информация о компании', blank=True)
    logo = models.ImageField('Изображение', upload_to=settings.MEDIA_COMPANY_IMAGE_DIR)
    employee_count = models.PositiveIntegerField('Количество сотрудников')

    owner = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='Владелец',
                                 related_name='company', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class Specialty(models.Model):
    title = models.CharField('Название', max_length=50, unique=True)
    code = models.CharField('Код', max_length=15, blank=True)
    picture = models.ImageField('Изображение', upload_to=settings.MEDIA_SPECIALITY_IMAGE_DIR)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'


class Skill(models.Model):
    title = models.CharField('Название', max_length=50, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'


class Vacancy(models.Model):
    title = models.CharField('Название вакансии', max_length=50)
    published_at = models.DateField('Дата размещения', auto_now_add=True)
    description = models.TextField('Описание', blank=True)
    salary_min = models.IntegerField('Зарплата от', null=True, blank=True)
    salary_max = models.IntegerField('Зарплата до', null=True, blank=True)
    is_remote = models.BooleanField('Удаленно')

    specialty = models.ForeignKey(Specialty, verbose_name='Специальность',
                                  related_name='vacancies', on_delete=models.CASCADE)

    company = models.ForeignKey(Company, verbose_name='Компания',
                                related_name='vacancies', on_delete=models.CASCADE)

    skills = models.ManyToManyField(Skill, verbose_name='Навыки')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'


class CustomUser(AbstractUser):
    is_company = models.BooleanField('Компания', default=False)


class Application(models.Model):
    written_username = models.CharField('Имя', max_length=50)
    written_phone = models.CharField('Телефон', max_length=20)
    written_cover_letter = models.TextField('Сопроводительное письмо')

    vacancy = models.ForeignKey(Vacancy, verbose_name='Вакансия',
                                related_name='applications', on_delete=models.CASCADE)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь', null=True, blank=True,
                             related_name='applications', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'

    def __str__(self):
        return self.pk


class Resume(models.Model):
    class WorkStatusChoices(models.TextChoices):
        NOT_IN_SEARCH = 'not_in_search', _('Не ищу работу')
        CONSIDERATION = 'consideration', _('Рассматриваю предложения')
        IN_SEARCH = 'in_search', _('Ищу работу')

    class EducationChoices(models.TextChoices):
        MISSING = 'missing', _('Отсутствует')
        SECONDARY = 'secondary', _('Среднее')
        VOCATIONAL = 'vocational', _('Средне-специальное')
        INCOMPLETE_HIGHER = 'incomplete_higher', _('Неполное высшее')
        HIGHER = 'higher', _('Высшее')

    class GradeChoices(models.TextChoices):
        INTERN = 'intern', _('intern')
        JUNIOR = 'junior', _('junior')
        MIDDLE = 'middle', _('middle')
        SENIOR = 'senior', _('senior')
        LEAD = 'lead', _('lead')

    name = models.CharField('Имя', max_length=50)
    surname = models.CharField('Фамилия', max_length=50)
    salary = models.PositiveIntegerField('Вознаграждение')
    experience = models.TextField('Опыт работы', blank=True)
    portfolio = models.URLField('Портфолио', max_length=300, blank=True)

    status = models.CharField('Готовность к работе', max_length=100,
                              choices=WorkStatusChoices.choices, default=WorkStatusChoices.IN_SEARCH)

    grade = models.CharField('Квалификация', max_length=50,
                             choices=GradeChoices.choices, default=GradeChoices.MIDDLE)

    education = models.CharField('Образование', max_length=30,
                                 choices=EducationChoices.choices, default=EducationChoices.HIGHER)

    institution = models.TextField('Учебное заведение')

    specialty = models.ForeignKey(Specialty, verbose_name='Специальность',
                                  related_name='resume', on_delete=models.CASCADE)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='Пользователь',
                                related_name='resume', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'

    def __str__(self):
        return f'{self.surname} {self.name}'
