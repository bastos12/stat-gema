from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()

class Statistique(models.Model):
    test_name = models.CharField(max_length=255)
    test_type = models.CharField(max_length=255)
    data = models.JSONField()
    p_value = models.FloatField()
    normality = models.FloatField()
    description = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f'test numero {self.id} {self.test_name}'
