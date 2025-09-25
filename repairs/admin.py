from django.contrib import admin
# добавил 02.08.25
from django.contrib import admin
from .models import Apartment, Room, Work, Material

admin.site.register(Apartment)
admin.site.register(Room)
admin.site.register(Work)
admin.site.register(Material)
