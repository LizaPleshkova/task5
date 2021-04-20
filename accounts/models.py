from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    STATUS_CHOICES = [
        ('Banned', 'Заблокирован'),
        ('Unbanned', 'Разблокирован'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField('Статус', choices=STATUS_CHOICES, max_length=30)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
