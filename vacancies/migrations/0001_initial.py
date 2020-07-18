# Generated by Django 3.0.7 on 2020-07-09 12:42

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False,
                                                     help_text=('Designates that this user has all '
                                                                'permissions without explicitly assigning them.'),
                                                     verbose_name='superuser status')),
                ('username', models.CharField(
                    error_messages={'unique': 'A user with that username already exists.'},
                    help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150,
                    unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                    verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False,
                                                 help_text='Designates whether the user can log into this admin site.',
                                                 verbose_name='staff status')),
                ('is_active', models.BooleanField(
                    default=True,
                    help_text=('Designates whether this user should be treated as active. '
                               'Unselect this instead of deleting accounts.'),
                    verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_company', models.BooleanField(verbose_name='Компания')),
                ('groups', models.ManyToManyField(
                    blank=True,
                    help_text=('The groups this user belongs to. '
                               'A user will get all permissions granted to each of their groups.'),
                    related_name='user_set', related_query_name='user', to='auth.Group',
                    verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.',
                                                            related_name='user_set', related_query_name='user',
                                                            to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Название')),
                ('location', models.CharField(max_length=30, verbose_name='Город')),
                ('description', models.TextField(blank=True, verbose_name='Информация о компании')),
                ('logo', models.ImageField(upload_to='company_images', verbose_name='Изображение')),
                ('employee_count', models.PositiveIntegerField(verbose_name='Количество сотрудников')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='company',
                                               to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Компания',
                'verbose_name_plural': 'Компании',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Навык',
                'verbose_name_plural': 'Навыки',
            },
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='Название')),
                ('code', models.CharField(blank=True, max_length=15, verbose_name='Код')),
                ('picture', models.ImageField(upload_to='speciality_images', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Специальность',
                'verbose_name_plural': 'Специальности',
            },
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название вакансии')),
                ('published_at', models.DateField(auto_now_add=True, verbose_name='Дата размещения')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('salary_min', models.IntegerField(blank=True, null=True, verbose_name='Зарплата от')),
                ('salary_max', models.IntegerField(blank=True, null=True, verbose_name='Зарплата до')),
                ('is_remote', models.BooleanField(verbose_name='Удаленно')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies',
                                              to='vacancies.Company', verbose_name='Компания')),
                ('skills', models.ManyToManyField(to='vacancies.Skill', verbose_name='Навыки')),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies',
                                                to='vacancies.Specialty', verbose_name='Специальность')),
            ],
            options={
                'verbose_name': 'Вакансия',
                'verbose_name_plural': 'Вакансии',
            },
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('surname', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('salary', models.PositiveIntegerField(verbose_name='Вознаграждение')),
                ('experience', models.TextField(blank=True, verbose_name='Опыт работы')),
                ('portfolio', models.URLField(blank=True, max_length=300, verbose_name='Портфолио')),
                ('status', models.CharField(
                    choices=[('not_in_search', 'Не ищу работу'), ('consideration', 'Рассматриваю предложения'),
                             ('in_search', 'Ищу работу')], default='in_search', max_length=100,
                    verbose_name='Готовность к работе')),
                ('grade', models.CharField(
                    choices=[('intern', 'intern'), ('junior', 'junior'), ('middle', 'middle'), ('senior', 'senior'),
                             ('lead', 'lead')], default='middle', max_length=50, verbose_name='Квалификация')),
                ('education', models.CharField(
                    choices=[('missing', 'Отсутствует'), ('secondary', 'Среднее'), ('vocational', 'Средне-специальное'),
                             ('incomplete_higher', 'Неполное высшее'), ('higher', 'Высшее')], default='higher',
                    max_length=30, verbose_name='Образование')),
                ('institution', models.TextField(verbose_name='Учебное заведение')),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resume',
                                                to='vacancies.Specialty', verbose_name='Специальность')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='resume',
                                              to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Резюме',
                'verbose_name_plural': 'Резюме',
            },
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('written_username', models.CharField(max_length=50, verbose_name='Имя')),
                ('written_phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('written_cover_letter', models.TextField(verbose_name='Сопроводительное письмо')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                           related_name='applications', to=settings.AUTH_USER_MODEL,
                                           verbose_name='Пользователь')),
                ('vacancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications',
                                              to='vacancies.Vacancy', verbose_name='Вакансия')),
            ],
            options={
                'verbose_name': 'Отклик',
                'verbose_name_plural': 'Отклики',
            },
        ),
    ]