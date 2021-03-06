# Generated by Django 3.2.5 on 2021-07-09 03:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("canvas", "0003_alter_node_t"),
    ]

    operations = [
        migrations.CreateModel(
            name="Connection",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "a",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Child",
                        to="canvas.node",
                    ),
                ),
                (
                    "b",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="canvas.node",
                    ),
                ),
            ],
        ),
    ]
