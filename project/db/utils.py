import random
import string

from django.utils.text import slugify


def get_random_string(size=5, chars=string.ascii_lowercase + string.digits):
    return ''.join([random.choice(chars) for _ in range(size)])


def get_unique_slug(instance, new_slug=None):
    print(instance.title,instance.slug)
    if new_slug is None:
        slug = slugify(instance.title)
    else:
        slug = new_slug
    Klass = instance.__class__ # Playlist, TVShow, Video
    qs = Klass.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        slug = slug + '-' + get_random_string()
        return get_unique_slug(instance, new_slug=slug)
    return slug
