from django.conf import settings
from django.db import models
from django.db.models import Sum, UniqueConstraint

from categories.models import Category
from project.db.models import BasicModel

# Create your models here.

User = settings.AUTH_USER_MODEL


def book_cover_path(instance, filename):
    return f'book_covers/{instance.slug}/{filename}'


class Viewers(BasicModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_viewers')
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE, related_name='user_viewers')
    count = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'viewer'
        verbose_name_plural = 'viewers'
        # UniqueConstraint(fields=['user', 'book'], name='unique_viewer')
        unique_together = ('user', 'book')

    def __str__(self):
        return f'{self.user} - {self.book} - {self.count} views'


class Book(BasicModel):
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    viewers = models.ManyToManyField(User, through=Viewers, related_name='viewed_books')
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    is_borrowed = models.BooleanField(default=False)

    @property
    def views(self):
        return self.user_viewers.aggregate(total_views=Sum('count'))['total_views']

    def increase_views(self, user):
        viewer, created = Viewers.objects.get_or_create(user=user, book=self)
        if not created:
            viewer.count += 1
            viewer.save()

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.title


class BookImage(BasicModel):
    image = models.ImageField(upload_to=book_cover_path)
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='image', null=True, blank=True)

    class Meta:
        verbose_name = 'Book Image'
        verbose_name_plural = 'Book Images'

    def __str__(self):
        return self.book.title
