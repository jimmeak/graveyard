# Generated by Django 2.0.13 on 2023-09-17 17:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0128_quests_encoding_20230917_1910"),
    ]

    operations = [
        migrations.AlterField(
            model_name="creationcomment",
            name="reputation",
            field=models.IntegerField(db_column="reputace", default=0),
        ),
    ]
