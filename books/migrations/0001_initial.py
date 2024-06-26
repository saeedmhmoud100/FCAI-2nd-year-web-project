# Generated by Django 5.0.6 on 2024-05-09 14:43

import books.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("categories", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Book",
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
                ("title", models.CharField(max_length=100)),
                ("author", models.CharField(max_length=100)),
                ("price", models.DecimalField(decimal_places=2, max_digits=5)),
                (
                    "cover",
                    models.ImageField(
                        blank=True, upload_to=books.models.book_cover_path
                    ),
                ),
                ("views", models.IntegerField(default=0)),
                ("description", models.TextField()),
                ("is_borrowed", models.BooleanField(default=False)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="books",
                        to="categories.category",
                    ),
                ),
                (
                    "uploaded_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="books",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
