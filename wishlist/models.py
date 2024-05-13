from django.conf import settings
from django.db import models

# Create your models here.

User = settings.AUTH_USER_MODEL

class UserWishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE, related_name='wishlist')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')
        verbose_name = 'User Wish List'
        verbose_name_plural = 'User Wish Lists'

    def __str__(self):
        return f'{self.user.username} - {self.product.title}'