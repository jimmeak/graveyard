# Generated by Django 2.0.2 on 2018-06-13 22:21

import ddcz.models.magic
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddcz', '0012_auto_20180614_0019'),
    ]

    operations = [
        migrations.AddField(
            model_name='monster',
            name='precteno',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='monster',
            name='autmail',
            field=ddcz.models.magic.MisencodedCharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='monster',
            name='autor',
            field=ddcz.models.magic.MisencodedCharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='monster',
            name='jmeno',
            field=ddcz.models.magic.MisencodedTextField(),
        ),
        migrations.AlterField(
            model_name='monster',
            name='pochvez',
            field=ddcz.models.magic.MisencodedIntegerField(default=0, max_length=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='monster',
            name='schvaleno',
            field=ddcz.models.magic.MisencodedCharField(choices=[('a', 'Schváleno'), ('n', 'Neschváleno')], max_length=1),
        ),
        migrations.AlterField(
            model_name='monster',
            name='zdroj',
            field=ddcz.models.magic.MisencodedTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='monster',
            name='zdrojmail',
            field=ddcz.models.magic.MisencodedCharField(blank=True, max_length=30, null=True),
        ),
    ]
