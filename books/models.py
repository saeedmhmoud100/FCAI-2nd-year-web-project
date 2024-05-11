from django.conf import settings
from django.db import models
from django.db.models import Sum, Avg
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from categories.models import Category
from project.db.models import BasicModel
from project.db.signals import unique_slugify_pre_save, slugify_book_image_post_save

# Create your models here.

User = settings.AUTH_USER_MODEL


def book_cover_path(instance, filename):
    return f'uploads/books/{instance.slug}/{filename}'


class Viewers(BasicModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='book_viewers', null=True)
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE, related_name='user_viewers')
    count = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'viewer'
        verbose_name_plural = 'viewers'
        # UniqueConstraint(fields=['user', 'book'], name='unique_viewer')
        unique_together = ('user', 'book')

    def __str__(self):
        return f'{self.user} - {self.book} - {self.count} views'


class queryset(models.QuerySet):
    def get_borrowed_by_user(self, user):
        return self.filter(borrower=user)


class BookManager(models.Manager):
    def get_queryset(self):
        return queryset(self.model, using=self._db)

    def active(self):
        return self.get_queryset().filter(active=True)

    def inactive(self):
        return self.get_queryset().filter(active=False)

    def available(self):
        return self.get_queryset().filter(is_borrowed=False)

    def borrowed(self):
        return self.get_queryset().filter(is_borrowed=True)


class Book(BasicModel):
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    viewers = models.ManyToManyField(User, through=Viewers, related_name='viewed_books')
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='borrowed_books', null=True, blank=True)
    objects = BookManager()

    def set_image(self, image):
        book_image, created = BookImage.objects.get_or_create(book=self)
        book_image.image = image
        book_image.save()

    @property
    def is_borrowed(self):
        return self.borrower is not None


    @property
    def rating(self):
        return self.ratings.aggregate(avg_rating=Avg('rating'))['avg_rating'] or '~'

    @property
    def views(self):
        return self.user_viewers.aggregate(total_views=Sum('count'))['total_views'] or 0

    def increase_views(self, user):
        viewer, created = Viewers.objects.get_or_create(user=user, book=self)
        if not created:
            viewer.count += 1
            viewer.save()

    def get_absolute_url(self):
        return reverse('book_details', args=[self.slug])

    @property
    def get_update_url(self):
        return reverse('update_book', args=[self.slug])

    def get_delete_url(self):
        return reverse('delete_book', args=[self.slug])

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.title


class BookImage(BasicModel):
    image = models.ImageField(upload_to=book_cover_path, null=True, blank=True)
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='image', null=True, blank=True)

    class Meta:
        verbose_name = 'Book Image'
        verbose_name_plural = 'Book Images'

    @property
    def url(self):
        return self.image.url

    def __str__(self):
        return self.book.title


pre_save.connect(unique_slugify_pre_save, sender=Book)
post_save.connect(slugify_book_image_post_save, sender=BookImage)
