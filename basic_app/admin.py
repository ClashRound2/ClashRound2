from django.contrib import admin
from basic_app.models import UserProfileInfo, Questions, submissions

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Questions)
admin.site.register(submissions)
