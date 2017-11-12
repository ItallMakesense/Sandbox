from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings

from .utils import unique_slug_generator
from .validators import validate_category


USER = settings.AUTH_USER_MODEL

class Outlet(models.Model):

    name = models.CharField(max_length=120)
    address = models.CharField(max_length=120, null=True,
                                blank=True)
    category = models.CharField(max_length=120, null=True,
                                blank=True, validators=[validate_category])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True, blank=True)
    owner = models.ForeignKey(USER)

    def __str__(self):
        return self.name

    @property
    def title(self):
        return self.name

def outlet_pre_save_receiver(sender, obj, *a, **kw):
    obj.category = obj.category.capitalize()
    if not obj.slug:
        obj.slug = unique_slug_generator(obj)

# def outlet_post_save_receiver(sender, instance, *a, **kw):
#     print('saved', instance.updated)

pre_save.connect(outlet_pre_save_receiver, sender=Outlet)

# post_save.connect(outlet_post_save_receiver, sender=Outlet)
