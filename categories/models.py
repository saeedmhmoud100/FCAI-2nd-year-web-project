from django.db import models

from project.db.models import BasicModel


# Create your models here.

class Category(BasicModel):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.title