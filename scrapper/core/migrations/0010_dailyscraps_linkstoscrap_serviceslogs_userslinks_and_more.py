# Generated by Django 4.1.2 on 2022-11-03 09:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0009_alter_mohitodailyscraps_toscrap_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyScraps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='LinksToScrap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=100)),
                ('item_name', models.CharField(max_length=50)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('service', models.CharField(max_length=20)),
                ('active', models.BooleanField(default=True)),
                ('deactivate_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServicesLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('error', models.CharField(max_length=20)),
                ('content', models.CharField(blank=True, max_length=1000, null=True)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('linktoscrap', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.linkstoscrap')),
            ],
        ),
        migrations.CreateModel(
            name='UsersLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('linktoscrap', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.linkstoscrap')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='mohitologs',
            name='toscrap',
        ),
        migrations.RemoveField(
            model_name='reserveddailyscraps',
            name='toscrap',
        ),
        migrations.RemoveField(
            model_name='reservedlogs',
            name='toscrap',
        ),
        migrations.RemoveField(
            model_name='zalandodailyscraps',
            name='zalandotoscrap',
        ),
        migrations.RemoveField(
            model_name='zalandologs',
            name='zalandotoscrap',
        ),
        migrations.DeleteModel(
            name='MohitoDailyScraps',
        ),
        migrations.DeleteModel(
            name='MohitoLogs',
        ),
        migrations.DeleteModel(
            name='MohitoToScrap',
        ),
        migrations.DeleteModel(
            name='ReservedDailyScraps',
        ),
        migrations.DeleteModel(
            name='ReservedLogs',
        ),
        migrations.DeleteModel(
            name='ReservedToScrap',
        ),
        migrations.DeleteModel(
            name='ZalandoDailyScraps',
        ),
        migrations.DeleteModel(
            name='ZalandoLogs',
        ),
        migrations.DeleteModel(
            name='ZalandoToScrap',
        ),
        migrations.AddField(
            model_name='dailyscraps',
            name='linktoscrap',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.linkstoscrap'),
        ),
    ]
