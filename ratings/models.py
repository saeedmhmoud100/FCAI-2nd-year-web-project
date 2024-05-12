from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save

from project.db.models import BasicModel
from ratings.db.signals import slugify_rating_post_save

# Create your models here.

User = settings.AUTH_USER_MODEL


class Rating(BasicModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE, related_name='ratings')
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    review = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'rating'
        verbose_name_plural = 'ratings'

    def __str__(self):
        return f'{self.user} - {self.book} - {self.rating}'


pre_save.connect(slugify_rating_post_save, sender=Rating)
