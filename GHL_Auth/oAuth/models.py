from django.db import models

# Create your models here.
class Api_Key_Data(models.Model):
    ghl_location_id = models.CharField(max_length=50, unique=True)
    ghl_location_name = models.TextField()
    ghl_oauth_token = models.CharField(max_length=50)
    ghl_refresh_token = models.CharField(max_length=50)
    ghl_oauth_token_expires_on = models.IntegerField()
    ghl_location_api_key = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)