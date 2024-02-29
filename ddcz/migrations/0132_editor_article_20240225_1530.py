# Generated by Django 2.0.13 on 2024-02-25 14:30

import ddcz.models.magic
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ddcz", "0131_letter_encoding_20240225_1412"),
    ]

    operations = [
        migrations.AlterField(
            model_name="editorarticle",
            name="text",
            field=ddcz.models.magic.MisencodedTextField(),
        ),
        migrations.AlterField(
            model_name="editorarticle",
            name="title",
            field=ddcz.models.magic.MisencodedCharField(
                max_length=40, verbose_name="Jméno"
            ),
        ),
    ]