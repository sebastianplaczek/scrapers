# Generated by Django 4.1.2 on 2022-11-03 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_dailyscraps_linkstoscrap_serviceslogs_userslinks_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceslogs',
            name='service',
            field=models.CharField(default='brak', max_length=20),
            preserve_default=False,
        ),
    ]
