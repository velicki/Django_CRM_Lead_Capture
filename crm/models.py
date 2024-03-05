from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class About(models.Model):
    body = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.body

class Lead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    topic = models.ForeignKey(Topic, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-update', '-created']

    def __str__(self):
        return self.name

