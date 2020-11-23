from django.db import models


class Bond(models.Model):
    isin = models.CharField(max_length=50)
    size = models.BigIntegerField()
    currency = models.CharField(max_length=10)
    maturity = models.DateField()
    lei = models.CharField(max_length=20)
    legal_name = models.CharField(max_length=100, default='N/A')
