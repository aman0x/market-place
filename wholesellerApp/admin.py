from django.contrib import admin
from.models import *

# admin.site.register(Wholeseller)


class wholeselleradmin(admin.ModelAdmin):
    list_display = ['id', 'wholeseller_name']