from django.db import models
from django.db.models.signals import pre_save, post_save

from .utils import unique_slug_generator


class Outlet(models.Model):
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=120, null=True,
                                blank=True)
    category = models.CharField(max_length=120, null=True,
                                blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def title(self):
        return self.name

def outlet_pre_save_receiver(sender, instance, *a, **kw):
    # print('saving...', instance.updated)
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

# def outlet_post_save_receiver(sender, instance, *a, **kw):
#     print('saved', instance.updated)

pre_save.connect(outlet_pre_save_receiver, sender=Outlet)

# post_save.connect(outlet_post_save_receiver, sender=Outlet)
