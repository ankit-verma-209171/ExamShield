# Generated by Django 3.2.5 on 2021-07-15 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0006_course_room_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='room_id',
            field=models.CharField(blank=True, default='room-<django.db.models.fields.CharField>', max_length=10),
        ),
    ]
