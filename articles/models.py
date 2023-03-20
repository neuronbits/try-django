from django.db import models
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
        if self.slug is None: # do only first time so if we change slug from admin then this is not called again
            self.slug = slugify(self.title)
        super.save(self, *args, **kwargs) # called original save method
        # obj. save ()
        # do another something
