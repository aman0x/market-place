from django.contrib import admin

# Register your models here.
from .models import Size, Colour, RetailerType, WholesellerType, Unit

# Register your models here.
admin.site.register([Size, Colour, RetailerType,
                    WholesellerType, Unit])
