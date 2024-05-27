from django.contrib import admin
from .models import Config
from config_models.admin import ConfigurationModelAdmin


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    pass
