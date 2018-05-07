from django.db import models


class TestModel(models.Model):
    created_at = models.DateTimeField(auto_created=True)
    update_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
