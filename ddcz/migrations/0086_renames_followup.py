# Generated by Django 2.0.13 on 2021-06-10 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ddcz", "0085_attribute_translations"),
    ]

    operations = [
        migrations.RenameField(
            model_name="alchemisttool",
            old_name="sphere",
            new_name="plane",
        ),
        migrations.RenameField(
            model_name="userprofile",
            old_name="last_access",
            new_name="last_login",
        ),
    ]
