from django.utils.text import slugify

from project.db.utils import get_unique_slug


def unique_slugify_pre_save(sender, instance, *args, **kwargs):
    instance.slug = get_unique_slug(instance,instance.slug)

def slugify_per_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        instance.slug = slugify(instance.title)

def slugify_book_image_post_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        instance.slug = slugify(instance.book.title + '-image')
        instance.save()