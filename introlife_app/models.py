from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length = 100)
    date = models.DateTimeField(auto_now_add = True)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    body = models.TextField()
    slug = models.SlugField(unique = True, null = True)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs = {'slug' : self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    