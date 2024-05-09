from django.conf import settings
from django.db import models

from project.db.models import BasicModel


# Create your models here.

User = settings.AUTH_USER_MODEL

class Rating(BasicModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='ratings')
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE, related_name='ratings')
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    review = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user} - {self.book} - {self.rating}'