from django.contrib import admin
from .models import (
    User,
    Statistique
)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Statistique)
class StatistiqueAdmin(admin.ModelAdmin):
    pass