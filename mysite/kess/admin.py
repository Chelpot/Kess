from django.contrib import admin

from .models import Kess


class KessAdmin(admin.ModelAdmin):
    fields = [ 'created_at', 'published_at', 'emoji', 'reponse', 'category', 'is_staff', 'is_ready_to_publish']
    list_display = ('reponse', 'emoji', 'created_at', 'category')
admin.site.register(Kess, KessAdmin)