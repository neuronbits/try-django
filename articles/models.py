from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(auto_now_add=False, auto_now=False, default=timezone.now) 
    # null=True for database to allow null, blank=True for form to allow empty, non mandatory

    def save(self, *args, **kwargs): # override save method. Here declared save method
        # obj = Article.objects.get (id=1)
        # set something
        #if self.slug is None: # do only first time so if we change slug from admin then this is not called again
        #    self.slug = slugify(self.title)
        super().save(*args, **kwargs) # called original save method
        # obj. save ()
        # do another something

def slugify_instance_title(instance, save=False):
    slug = slugify(instance.title)
    qs = Article.objects.filter(slug=slug).exclude(id=instance.id) # exclude current instance. i.e like ignore(id) in update function
    if qs.exists():
        slug = f'{slug}-{qs.count()+1}'
    instance.slug = slug
    if save:
        instance.save() # calling save because this is after save i.e post_save so we have to manually call
    return instance # optional

# this signal is alrternative to what we did above in save method
def article_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance_title(instance, save=False)

pre_save.connect(article_pre_save, sender=Article)
 
def article_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_title(instance, save=True)

post_save.connect(article_post_save, sender=Article)
