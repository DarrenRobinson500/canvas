# Generated by Django 3.2.5 on 2021-07-12 02:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("canvas", "0021_alter_db_visible"),
    ]

    operations = [
        migrations.AlterField(
            model_name="connection",
            name="a",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="Child",
                to="canvas.db",
            ),
        ),
        migrations.AlterField(
            model_name="connection",
            name="b",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="canvas.db",
            ),
        ),
    ]
