from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

from project.db.models import BasicModel
from ratings.db.signals import slugify_rating_post_save

# Create your models here.

User = settings.AUTH_USER_MODEL


class RatingQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)
class RatingManager(models.Manager):
    def get_queryset(self):
        return RatingQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

class Rating(BasicModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE, related_name='ratings')
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    review = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

    objects = RatingManager()

    def change_active(self):
        self.active = not self.active
        self.save()

    @property
    def get_check_active_url(self):
        return reverse('rating_change_active', kwargs={'slug': self.slug, 'book_slug': self.book.slug})
    def get_delete_url(self):
        return reverse('delete_rating', kwargs={'slug': self.slug, 'book_slug': self.book.slug})
    class Meta:
        verbose_name = 'rating'
        verbose_name_plural = 'ratings'

    def __str__(self):
        return f'{self.user} - {self.book} - {self.rating}'


pre_save.connect(slugify_rating_post_save, sender=Rating)
