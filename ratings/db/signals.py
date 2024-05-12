from django.utils.text import slugify

from project.db.utils import get_unique_slug


def slugify_rating_post_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        instance.slug = slugify(instance.book.title+instance.user.username + '-rating')
        instance.save()