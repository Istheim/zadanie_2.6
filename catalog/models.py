from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name='наименование')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    image = models.ImageField(upload_to='preview/', verbose_name='превью', **NULLABLE)
    category = models.CharField(max_length=100, verbose_name='категория')
    price = models.PositiveIntegerField(verbose_name='цена за покупку')
    first_data = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    last_data = models.DateTimeField(verbose_name='дата последнего изменения')

    def __str__(self):
        return f'{self.title} {self.price} {self.category}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name='наименование')
    description = models.TextField(verbose_name='описание')
    #created_at = models.DateTimeField(auto_now_add=True, verbose_name='когда был создан')

    def __str__(self):
        return f'{self.title} {self.description}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
