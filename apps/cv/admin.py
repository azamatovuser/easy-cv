from django.contrib import admin
from apps.cv.models import Cv


@admin.register(Cv)
class CvAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'prompt')
    list_filter = ('user__username', )