from django.db import models


# Create your models here.

class User(models.Model):

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)

    bio = models.TextField(blank=True)

    birthDate = models.DateField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
