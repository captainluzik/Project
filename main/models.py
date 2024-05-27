from django.db import models
from config_models.models import ConfigurationModel


class Config(ConfigurationModel):
    login = models.CharField(max_length=100, default='login')
    password = models.CharField(max_length=100, default='password')

    class Meta:
        verbose_name = 'Настройки'
        verbose_name_plural = 'Настройки'
