from django.contrib import admin

# Register your models here.
from .models import LastNotice,Profile

admin.site.register(LastNotice)
admin.site.register(Profile)
