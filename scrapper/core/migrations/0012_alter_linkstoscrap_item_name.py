# Generated by Django 4.1.2 on 2022-11-06 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_serviceslogs_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkstoscrap',
            name='item_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
