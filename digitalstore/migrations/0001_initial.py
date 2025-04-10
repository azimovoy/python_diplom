# Generated by Django 5.1.4 on 2024-12-09 13:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Категория')),
                ('icon', models.ImageField(blank=True, null=True, upload_to='icons/', verbose_name='Иконка')),
                ('slug', models.SlugField(null=True, unique=True, verbose_name='Поле слаг')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='digitalstore.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название товара')),
                ('price', models.FloatField(verbose_name='Цена')),
                ('quantity', models.IntegerField(default=0, verbose_name='В наличии')),
                ('color_name', models.CharField(max_length=100, verbose_name='Название цвета')),
                ('color_code', models.CharField(max_length=10, verbose_name='Код цвета')),
                ('slug', models.SlugField(null=True, unique=True, verbose_name='Слаг товара')),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_images/', verbose_name='Картинка товара')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='digitalstore.category', verbose_name='Категория товара')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
    ]
