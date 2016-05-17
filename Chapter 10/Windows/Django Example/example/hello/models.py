from django.db import models

class Counter(models.Model):
    count = models.IntegerField()

