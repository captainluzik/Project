from django.db import models


class Config(models.Model):
    login = models.CharField(max_length=100, default='login')
    password = models.CharField(max_length=100, default='password')

    class Meta:
        verbose_name = 'Настройки'
        verbose_name_plural = 'Настройки'

    def __str__(self):
        return self.login
