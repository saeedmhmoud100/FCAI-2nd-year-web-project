# Generated by Django 5.0.6 on 2024-05-09 21:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0003_rename_cover_book_image"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="book",
            options={"verbose_name": "Book", "verbose_name_plural": "Books"},
        ),
        migrations.AlterModelOptions(
            name="bookimage",
            options={
                "verbose_name": "Book Image",
                "verbose_name_plural": "Book Images",
            },
        ),
        migrations.CreateModel(
            name="Viewers",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("slug", models.SlugField(unique=True)),
                ("active", models.BooleanField(default=True)),
                ("order", models.IntegerField(default=1)),
                ("count", models.IntegerField(default=0)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_viewers",
                        to="books.book",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="book_viewers",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "viewer",
                "verbose_name_plural": "viewers",
            },
        ),
        migrations.AddField(
            model_name="book",
            name="viewers",
            field=models.ManyToManyField(
                related_name="viewed_books",
                through="books.Viewers",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]