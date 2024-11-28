from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Activity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    image = models.ImageField(upload_to="media")

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    lieu = models.CharField(max_length=200)
    image = models.ImageField(upload_to="media")

    def __str__(self):
        return self.title

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog")
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to="media", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    nb_vues = models.IntegerField(default=0)

    def calculer_nb_vue(self):
        self.nb_vues += 1
        self.save()

    @classmethod
    def get_popular_blogs(cls):
        return cls.objects.all().order_by('-nb_vues')

    def __str__(self):
        return self.title