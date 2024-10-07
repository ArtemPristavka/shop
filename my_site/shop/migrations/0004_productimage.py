# Generated by Django 5.1.1 on 2024-10-07 11:18

import django.db.models.deletion
import shop.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(default=False, null=True, upload_to=shop.models.generic_path_to_save_photo)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='shop.product')),
            ],
        ),
    ]
