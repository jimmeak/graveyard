# Generated by Django 2.0.13 on 2021-09-04 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ddcz", "0104_runes_and_userrating_table"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="UzivateleCekajici",
            new_name="AwaitingRegistration",
        ),
        migrations.RenameModel(
            old_name="Letters",
            new_name="Letter",
        ),
        migrations.RenameModel(
            old_name="Runes",
            new_name="Rune",
        ),
        migrations.RenameModel(
            old_name="UserRatings",
            new_name="UserRating",
        ),
        migrations.AlterUniqueTogether(
            name="awaitingregistration",
            unique_together=set(),
        ),
    ]