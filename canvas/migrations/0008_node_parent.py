# Generated by Django 3.2.5 on 2021-07-10 22:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('canvas', '0007_auto_20210710_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='canvas.node'),
        ),
    ]
