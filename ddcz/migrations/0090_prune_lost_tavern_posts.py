# Generated by Django 2.0.13 on 2021-06-12 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ddcz", "0089_tavern_comment_post"),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                (
                    """
            DELETE FROM
                `putyka_prispevky`
            WHERE
                id_stolu = 0
            """
                )
            ],
            reverse_sql=[],
        ),
    ]