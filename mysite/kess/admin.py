from django.contrib import admin

from .models import Kess, User, Tile


class KessAdmin(admin.ModelAdmin):
    fields = ['created_at',
              'created_by',
              'published_at',
              'emoji',
              'reponse',
              'category',
              'is_staff',
              'is_ready_to_publish',
              'foundList',
              'nbTries']
    list_display = ('reponse', 'emoji', 'created_at', 'created_by', 'published_at', 'category', 'foundList', 'nbTries')


class UserAdmin(admin.ModelAdmin):
    fields = ['email', 'name', 'avatar', 'points', 'favs', 'is_superuser', 'creation_date']
    list_display = ('email', 'name', 'avatar', 'points', 'favs', 'is_superuser', 'creation_date')


class TileAdmin(admin.ModelAdmin):
    fields = ['avatar', 'name', 'action', 'time']
    list_display = ('avatar', 'name', 'action', 'time')


admin.site.register(Kess, KessAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Tile, TileAdmin)
