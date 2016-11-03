from django.contrib import admin

# Register your models here.
from .models import Race, Series

admin.site.register(Race)
admin.site.register(Series)
