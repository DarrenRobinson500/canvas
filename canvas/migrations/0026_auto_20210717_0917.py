# Generated by Django 3.2.5 on 2021-07-16 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canvas', '0025_auto_20210716_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='db',
            name='date_due',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='db',
            name='frequency',
            field=models.CharField(blank=True, choices=[('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly'), ('Quarterly', 'Quarterly'), ('Yearly', 'Yearly')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='db',
            name='impact_i',
            field=models.CharField(blank=True, choices=[('1', 'Insignificant'), ('2', 'Minor'), ('3', 'Moderate'), ('4', 'Major'), ('5', 'Severe')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='db',
            name='impact_r',
            field=models.CharField(blank=True, choices=[('1', 'Insignificant'), ('2', 'Minor'), ('3', 'Moderate'), ('4', 'Major'), ('5', 'Severe')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='db',
            name='likelihood_i',
            field=models.CharField(blank=True, choices=[('1', 'Rare (1) <10%'), ('2', 'Unlikely (2) 10% - 25%'), ('3', 'Possible (3) 25% - 50%'), ('4', 'Likely (4) 50% - 80%'), ('5', 'Almost Certain (5) > 80%')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='db',
            name='likelihood_r',
            field=models.CharField(blank=True, choices=[('1', 'Rare (1) <10%'), ('2', 'Unlikely (2) 10% - 25%'), ('3', 'Possible (3) 25% - 50%'), ('4', 'Likely (4) 50% - 80%'), ('5', 'Almost Certain (5) > 80%')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='db',
            name='type',
            field=models.CharField(blank=True, choices=[('role', 'role'), ('busobj', 'busobj'), ('obligation', 'obligation'), ('process', 'process'), ('risk', 'risk'), ('metric', 'metric'), ('control', 'control'), ('issue', 'issue'), ('action', 'action')], max_length=255, null=True),
        ),
    ]
