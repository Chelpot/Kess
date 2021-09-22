from django.contrib import admin

from .models import Kess


class KessAdmin(admin.ModelAdmin):
    fields = ['date', 'emoji', 'reponse', 'isStaff']
    list_display = ('reponse', 'emoji', 'date')
admin.site.register(Kess, KessAdmin)