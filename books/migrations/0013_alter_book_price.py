# Generated by Django 5.0.6 on 2024-05-13 17:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0012_alter_bookimage_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="price",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
