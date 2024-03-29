# Generated by Django 4.1.2 on 2022-10-10 17:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_zalandodailyscraps_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZalandoLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('error', models.CharField(max_length=1000)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('zalandotoscrap', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.zalandotoscrap')),
            ],
        ),
    ]
