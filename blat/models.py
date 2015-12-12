from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Blat(models.Model):
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    via = models.URLField(blank=True)
    created_by = models.ForeignKey(User)
    category = models.ForeignKey(Category)

    @property
    def total_likes(self):
        return self.like_set.count()

    def has_user_liked_it(self, id):
        return any(like.owner.id == id
                   for like in self.like_set.all())

    def __str__(self):
        return self.text[:50]


class Like(models.Model):
    blat = models.ForeignKey(Blat)
    owner = models.ForeignKey(User)


class Profile(models.Model):
    user = models.OneToOneField(User)
    bio = models.TextField(blank=True)
    blog = models.URLField(blank=True)
