from project.db.utils import get_unique_slug


def unique_slugify_pre_save(sender, instance, *args, **kwargs):
    instance.slug = get_unique_slug(instance,instance.slug)
