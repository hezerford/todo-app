from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model): # Таблица категория которая наследует models.Model
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, verbose_name='Название категории') #varchar.Нам потребуется только имя категории
    class Meta:
        verbose_name = ("Category") # человекочитаемое имя объекта
        verbose_name_plural = ("Categories")  #человекочитаемое множественное имя для Категорий
    def __str__(self):
        return self.name  # __str__ применяется для отображения объекта в интерфейсе

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Имя пользователя')
    title = models.CharField(max_length=200, verbose_name='Название задачи')
    description = models.TextField(max_length=500, null=True, blank=True, verbose_name='Описание')
    complete = models.BooleanField(default=False, verbose_name='Выполнена?')
    create = models.DateTimeField(default=timezone.now)  # Изменено здесь
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Категория')
    due_date = models.DateField(default=timezone.now)  # Изменено здесь

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete', '-create']