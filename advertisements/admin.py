from django.contrib import admin

from .models import  Advertisement, Favorite


# Register your models here.
@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'status', 'creator', 'created_at', 'updated_at']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'favorite', 'user']