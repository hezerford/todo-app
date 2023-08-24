from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Имя пользователя')
    title = models.CharField(max_length=200, verbose_name='Название задачи')
    description = models.TextField(max_length=500,null=True, blank=True, verbose_name='Описание')
    complete = models.BooleanField(default=False, verbose_name='Выполнена?')
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']