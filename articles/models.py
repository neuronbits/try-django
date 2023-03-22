from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.utils import timezone
from .utils import slugify_instance_title

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(auto_now_add=False, auto_now=False, default=timezone.now) 
    # null=True for database to allow null, blank=True for form to allow empty, non mandatory

    def get_absolute_url(self):
        #return f'/articles/{self.slug}/'
        return reverse('article-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # override save method. Here declared save method
        # obj = Article.objects.get (id=1)
        # set something
        #if self.slug is None: # do only first time so if we change slug from admin then this is not called again
        #    self.slug = slugify(self.title)

        # below can also be used as we did above. in this case we dont use pre method at very bottom. we can comment that function
        # but best is to use pre and post at very bottom
        # if self.slug is None:
        #     slugify_instance_title(self, save=False)
                       
        super().save(*args, **kwargs) # called original save method
        # obj. save ()
        # do another something

# this signal is alrternative to what we did above in save method
def article_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance_title(instance, save=False)

pre_save.connect(article_pre_save, sender=Article)
 
def article_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_title(instance, save=True)

post_save.connect(article_post_save, sender=Article)
