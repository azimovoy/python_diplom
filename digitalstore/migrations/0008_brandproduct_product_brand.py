# Generated by Django 5.1.4 on 2024-12-21 10:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digitalstore', '0007_alter_product_accumulator_alter_product_back_camera_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrandProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название Бренда (Марка)')),
            ],
            options={
                'verbose_name': 'Бранд',
                'verbose_name_plural': 'Бренды',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='digitalstore.brandproduct', verbose_name='Бренд товара'),
        ),
    ]
