# apps/accounts/models.py
from django.db import models
import random
import string

class EmailVerificationCode(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)  # Поле для даты создания

    def generate_new_code(self):
        self.code = str(random.randint(10000, 99999))  # Генерация 5-значного кода
        self.save()  # Сохраняем изменения в базе данных
