# Generated by Django 3.2.5 on 2021-07-14 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='is_given',
            field=models.BooleanField(default=False),
        ),
    ]
