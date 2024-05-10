from django.db import models
from django.db.models.signals import pre_save

from project.db.signals import unique_slugify_pre_save


class BasicModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=True, editable=False)
    active = models.BooleanField(default=True)
    order = models.IntegerField(default=1)


    class Meta:
        abstract = True
