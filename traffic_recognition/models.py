from django.db import models

# Create your models here.
class High_risk_traffic(models.Model):
        proto = models.IntegerField()
        src_ip = models.CharField(max_length= 15)
        des_ip = models.CharField(max_length=15)
        sport = models.IntegerField()
        dsport = models.IntegerField()
        load = models.CharField(max_length=1024)
