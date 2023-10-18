from django.db import models

# Create your models here.
class Authtokendata(models.Model):
    access_token = models.TextField()
    companyId = models.CharField(max_length=100)
    access_expires_in = models.IntegerField()
    locationId = models.CharField(max_length=100, unique=True)
    refresh_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.locationId