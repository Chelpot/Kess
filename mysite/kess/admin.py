from django.contrib import admin

from .models import Kess, User


class KessAdmin(admin.ModelAdmin):
    fields = ['created_at',
              'published_at',
              'emoji',
              'reponse',
              'category',
              'is_staff',
              'is_ready_to_publish',
              'foundList']
    list_display = ('reponse', 'emoji', 'created_at', 'category', 'foundList')


class UserAdmin(admin.ModelAdmin):
    fields = ['email', 'name', 'points', 'is_superuser', 'creation_date']
    list_display = ('email', 'name', 'points', 'is_superuser', 'creation_date')


admin.site.register(Kess, KessAdmin)
admin.site.register(User, UserAdmin)
