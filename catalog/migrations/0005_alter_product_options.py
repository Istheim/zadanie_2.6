# Generated by Django 4.2.4 on 2023-09-08 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_contact_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'permissions': [('set_published', 'Can publish postscreate_product')], 'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
    ]
