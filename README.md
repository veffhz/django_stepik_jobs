Job search project with Django
==================  
[![Heroku](https://heroku-badge.herokuapp.com/?app=django-stepik-jobs&style=flat)](https://django-stepik-jobs.herokuapp.com)

##### features:
 - index page (specialties, companies blocks)
 - search vacancies by skills
 - companies, company page
 - vacancies, vacancy page
 - create own company
 - public vacancies
 - public resume
 
##### requirements:
 - Python 3.6+
 - Django 3
 - Gunicorn 20+

##### install requirements:
`pip3 install -r requirements.txt`

##### run app:
 - run `python manage.py migrate`
 - run `python manage.py import_data`
 - run `gunicorn jobs_project.wsgi`
 - open default page http://127.0.0.1:8000/
 
##### you can login with pre-fill accounts: 
 - `admin/admin`
 - `test_user_1/Password1` - `test_user_8/Password8`
