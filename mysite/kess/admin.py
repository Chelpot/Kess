from django.contrib import admin

from .models import Kess


class KessAdmin(admin.ModelAdmin):
    fields = ['date', 'emoji', 'reponse', 'isStaff', 'category']
    list_display = ('reponse', 'emoji', 'date', 'category')
admin.site.register(Kess, KessAdmin)