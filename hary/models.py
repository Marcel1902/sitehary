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