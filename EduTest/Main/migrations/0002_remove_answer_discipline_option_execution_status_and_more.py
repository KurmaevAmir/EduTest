# Generated by Django 5.0.6 on 2024-07-02 12:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='discipline',
        ),
        migrations.AddField(
            model_name='option',
            name='execution_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='test',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.profile'),
        ),
        migrations.DeleteModel(
            name='IssuingTest',
        ),
    ]
