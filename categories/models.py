from django.db import models
from django.db.models.signals import pre_save

from project.db.models import BasicModel
from project.db.signals import unique_slugify_pre_save


# Create your models here.

class Category(BasicModel):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.title


pre_save.connect(unique_slugify_pre_save, sender=Category)
