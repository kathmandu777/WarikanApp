from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class Meta(AbstractUser.Meta):
        verbose_name_plural = 'CustomUser'  # 複数形の名前もCustomUserにしておく
