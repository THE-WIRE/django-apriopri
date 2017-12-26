"""
Models definition
"""

from django.db import models

class Upload(models.Model):
    """To handle uploaded files"""
    test_name = models.CharField(max_length=200)
    datafile = models.FileField()
    upload_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.test_name + ' | ' + str(self.upload_date)


class Data(models.Model):
    """To handle data acquired from uploaded files"""
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)
    sr = models.IntegerField()
    basket_value = models.FloatField()
    recency_days = models.FloatField()
    items = models.CharField(max_length=2000)
