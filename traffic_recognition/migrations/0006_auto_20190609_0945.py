# Generated by Django 2.2.2 on 2019-06-09 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('traffic_recognition', '0005_auto_20190609_0944'),
    ]

    operations = [
        migrations.RenameField(
            model_name='high_risk_traffic',
            old_name='dsport',
            new_name='dport',
        ),
    ]
