from django.contrib import admin
from apps.cv.models import Cv, Contact


@admin.register(Cv)
class CvAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'prompt')
    list_filter = ('user__username', )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    list_filter = ('name', 'email')