# Generated by Django 2.0.13 on 2020-11-09 17:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0044_download_item_data"),
    ]

    operations = [
        migrations.AddField(
            model_name="downloaditem",
            name="download_counter",
            field=models.IntegerField(default=0),
        ),
    ]