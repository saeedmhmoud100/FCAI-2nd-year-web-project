# Generated by Django 5.0.6 on 2024-05-13 22:15

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0013_alter_book_price"),
        ("wishlist", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="userwishlist",
            unique_together={("user", "book")},
        ),
    ]
