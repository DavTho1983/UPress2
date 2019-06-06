from django.db import models


class Expression(models.Model):
    expression = models.CharField(max_length=255)
    result = models.IntegerField(null=True)