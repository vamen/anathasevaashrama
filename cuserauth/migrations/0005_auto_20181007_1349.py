# Generated by Django 2.1 on 2018-10-07 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuserauth', '0004_auto_20181007_0809'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lecturers',
            old_name='toaken',
            new_name='token',
        ),
    ]
