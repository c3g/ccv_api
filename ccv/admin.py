# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Address, Email, Identification, LanguageSkill, Telephone, Website, Degree, Supervisor,\
    UserProfile, PersonalInformation

admin.site.register(Address)
admin.site.register(Telephone)
admin.site.register(Email)
admin.site.register(Identification)
admin.site.register(LanguageSkill)
admin.site.register(Website)
admin.site.register(Degree)
admin.site.register(Supervisor)
admin.site.register(UserProfile)
admin.site.register(PersonalInformation)

