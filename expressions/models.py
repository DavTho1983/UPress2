from django.db import models


class Expression(models.Model):
    expression = models.TextField()
    result = models.IntegerField()