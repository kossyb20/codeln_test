from django.db import models

# Create your models here.

class Person(models.Model):
    email = models.CharField(max_length=255, blank=False, null=False)
    password = models.CharField(max_length=16, blank=False, null=False)
    ip_address = models.CharField(max_length=255, blank=False, null=False)
    fail_login_attempts = models.IntegerField()

    def __str__(self):
        return self.email
