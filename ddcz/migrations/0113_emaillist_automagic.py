# Generated by Django 2.0.13 on 2021-09-04 19:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0112_emaillist_autofill"),
    ]

    operations = [
        migrations.RunSQL("ALTER TABLE `uzivatele_maillist` DROP PRIMARY KEY;"),
        migrations.RunSQL(
            "ALTER TABLE uzivatele_maillist MODIFY django_id INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY;"
        ),
        migrations.RunSQL(
            """
                SET @m = (SELECT IFNULL(MAX(django_id) + 1, 1) FROM uzivatele_maillist);
                SET @s = CONCAT('ALTER TABLE uzivatele_maillist AUTO_INCREMENT=', @m);
                PREPARE stmt1 FROM @s;
                EXECUTE stmt1;
                DEALLOCATE PREPARE stmt1;
            """
        ),
    ]
