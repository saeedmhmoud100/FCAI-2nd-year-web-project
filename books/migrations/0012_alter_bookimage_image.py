# Generated by Django 5.0.6 on 2024-05-11 12:26

import books.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0011_remove_book_is_borrowed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bookimage",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to=books.models.book_cover_path
            ),
        ),
    ]
