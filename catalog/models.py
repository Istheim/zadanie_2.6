from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from builtins import *

NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name='наименование')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    image = models.ImageField(upload_to='preview/', verbose_name='превью', **NULLABLE)
    category = models.CharField(max_length=100, verbose_name='категория')
    price = models.PositiveIntegerField(verbose_name='цена за покупку')
    first_data = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    last_data = models.DateTimeField(verbose_name='дата последнего изменения')
    is_active = models.BooleanField(default=True, verbose_name='опубликован')

    user_boss = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                                  verbose_name='Продавец')

    def __str__(self):
        return f'{self.title} {self.price} {self.category}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

        permissions = [
            (
                'set_published',
                'Can publish posts'
            )
        ]


class Category(models.Model):
    name_category = models.CharField(max_length=100, verbose_name='Наименование категории', default='Значение по '
                                                                                                    'умолчанию')
    category_description = models.CharField(max_length=100, verbose_name='Описание категории', default='Значение по '
                                                                                                       'умолчанию')

    def __str__(self):
        return f'{self.name_category} {self.category_description}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Version(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    version_number = models.CharField(max_length=10, verbose_name='Номер версии')
    version_name = models.CharField(max_length=100, verbose_name='Название версии')
    is_current = models.BooleanField(default=False, verbose_name='Активность')

    # def save(self, *args, **kwargs):
    #     if self.is_current:
    #         # При установке этой версии как активной,
    #         # устанавливаем все остальные версии для этого продукта как неактивные
    #         Version.objects.filter(product=self.product).exclude(pk=self.pk).update(is_current=False)
    #     super(Version, self).save(*args, **kwargs)
    def __str__(self):
        return f'{self.product}, {self.version_name}, {self.version_number}'

    class Meta:
        verbose_name = "версия"
        verbose_name_plural = "версии"


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    phone = models.IntegerField(unique=True, null=False, blank=False)
    message = models.TextField(verbose_name='message')

    def __str__(self):
        return self.name


def toggle_activity(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    if product_item.is_active:
        product_item.is_active = False
    else:
        product_item.is_active = True

    product_item.save()

    return redirect(reverse('home'))
