from django.contrib import admin

# Register your models here.
from .models import State, District, City

# Register your models here.
admin.site.register([State, District, City])
