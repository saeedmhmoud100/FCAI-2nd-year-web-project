# Generated by Django 5.0.6 on 2024-05-09 14:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0002_bookimage_alter_book_cover"),
    ]

    operations = [
        migrations.RenameField(
            model_name="book",
            old_name="cover",
            new_name="image",
        ),
    ]