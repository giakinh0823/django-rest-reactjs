# Generated by Django 3.0 on 2021-07-22 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20210722_2256'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, max_length=2000, null=True, upload_to='product/products'),
        ),
    ]