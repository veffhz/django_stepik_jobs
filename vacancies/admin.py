from django.contrib import admin

from .models import (
    Vacancy,
    Specialty,
    Company,
    Application,
    Resume,
    Skill
)

admin.site.register(Vacancy)
admin.site.register(Skill)
admin.site.register(Specialty)
admin.site.register(Company)
admin.site.register(Application)
admin.site.register(Resume)
