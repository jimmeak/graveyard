# Generated by Django 2.0.13 on 2021-09-04 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ddcz", "0109_emaillist_columns"),
    ]

    operations = [
        migrations.RenameField(
            model_name="creationemailsubscription",
            old_name="rubrika",
            new_name="creative_page_slug",
        ),
        migrations.RenameField(
            model_name="creationemailsubscription",
            old_name="email_uz",
            new_name="user_email",
        ),
        migrations.RenameField(
            model_name="creationemailsubscription",
            old_name="id_uz",
            new_name="user_profile_id",
        ),
        migrations.AlterUniqueTogether(
            name="creationemailsubscription",
            unique_together={("user_profile_id", "creative_page_slug")},
        ),
    ]
