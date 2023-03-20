import random
from django.utils.text import slugify


def slugify_instance_title(instance, save=False, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__ # ths reason for this is it can be run on any other model. generic way
    qs = Klass.objects.filter(slug=slug).exclude(id=instance.id) # exclude current instance. i.e like ignore(id) in update function
    #qs = Article.objects.filter(slug=slug).exclude(id=instance.id) # exclude current instance. i.e like ignore(id) in update function
    if qs.exists():
        rand_int = random.randint(300_000,500_000) # 300K to 500K
        slug = f'{slug}-{rand_int}' # auto generating new slug
        return slugify_instance_title(instance, save=False, new_slug=slug) # recursion untill find unique slug
    instance.slug = slug
    
    if save:
        instance.save() # calling save because this is after save i.e post_save so we have to manually call
    return instance # optional
