# Generated by Django 3.2.5 on 2021-07-17 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canvas', '0027_auto_20210717_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='db',
            name='date_performed',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='db',
            name='type',
            field=models.CharField(blank=True, choices=[('role', 'role'), ('busobj', 'busobj'), ('obligation', 'obligation'), ('process', 'process'), ('risk', 'risk'), ('metric', 'metric'), ('control', 'control'), ('control_inst', 'control_inst'), ('control_test', 'control_test'), ('issue', 'issue'), ('action', 'action')], max_length=255, null=True),
        ),
    ]
