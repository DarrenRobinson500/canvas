# Generated by Django 3.2.5 on 2021-07-17 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canvas', '0029_db_outcome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='db',
            name='date_due',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='db',
            name='date_first',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='db',
            name='date_performed',
            field=models.DateField(blank=True, null=True),
        ),
    ]