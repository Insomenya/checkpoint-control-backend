# Generated by Django 4.0.6 on 2025-04-15 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'зона',
                'verbose_name_plural': 'зоны',
            },
        ),
        migrations.CreateModel(
            name='Checkpoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('zone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkpoints.zone', verbose_name='Зона')),
            ],
            options={
                'verbose_name': 'КПП',
                'verbose_name_plural': 'КПП',
            },
        ),
    ]
