from django.db import models


class BasicModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=50, unique=True)
    active = models.BooleanField(default=True)
    order = models.IntegerField(default=1)


    class Meta:
        abstract = True
