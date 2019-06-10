from django.db import models

# Create your models here.
class High_risk_traffic(models.Model):
        id = models.IntegerField(primary_key=True)
        proto = models.IntegerField()
        src_ip = models.CharField(max_length= 15)
        dst_ip = models.CharField(max_length=15)
        sport = models.CharField(max_length=10)
        dport = models.CharField(max_length=10)

class black_list(models.Model):
        id = models.IntegerField(primary_key=True)
        ip = models.CharField(max_length=15)