from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    title_post = models.CharField(max_length=25, verbose_name='Заголовок статьи')
    content_post = models.CharField(max_length=5000, verbose_name='Содержание статьи')
    image_post = models.ImageField(upload_to='preview', verbose_name='Изображение', **NULLABLE)
    data_post = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    # публикации,
    publication_on_off = models.BooleanField(default=True, verbose_name='Опубликовано')
    # просмотры.
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')
    slug = models.CharField(max_length=100, verbose_name='slug', **NULLABLE)

    def __str__(self):
        return f'{self.title_post} {self.image_post} {self.data_post}'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
