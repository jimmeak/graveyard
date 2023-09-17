# Generated by Django 2.0.13 on 2021-04-28 12:28

from django.db import migrations, models


def fill_relation_table_ids(apps, schema_editor):
    Relation = apps.get_model("ddcz", "TavernBookmark")
    i = 1
    for relation in Relation.objects.all():
        Relation.objects.filter(
            id_stolu=relation.id_stolu, id_uz=relation.id_uz
        ).update(django_id=i)
        i += 1


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0072_tavern_model_renames"),
    ]

    operations = [
        migrations.AddField(
            model_name="tavernbookmark",
            name="django_id",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.RunPython(fill_relation_table_ids),
        migrations.RunSQL("ALTER TABLE `putyka_book` DROP PRIMARY KEY;"),
        migrations.RunSQL(
            "ALTER TABLE putyka_book MODIFY django_id INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY;"
        ),
        migrations.RunSQL(
            """
                SET @m = (SELECT IFNULL(MAX(django_id) + 1, 1) FROM putyka_book);
                SET @s = CONCAT('ALTER TABLE putyka_book AUTO_INCREMENT=', @m);
                PREPARE stmt1 FROM @s;
                EXECUTE stmt1;
                DEALLOCATE PREPARE stmt1;
            """
        ),
        migrations.AlterField(
            model_name="tavernbookmark",
            name="django_id",
            field=models.IntegerField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="tavernbookmark",
            name="id_stolu",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="tavernbookmark",
            name="django_id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
