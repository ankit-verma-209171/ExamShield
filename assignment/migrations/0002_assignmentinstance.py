# Generated by Django 3.2.5 on 2021-07-09 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_auto_20210708_1850'),
        ('assignment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignmentInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submit_time', models.DateTimeField(auto_now=True)),
                ('file_uploaded', models.FileField(upload_to='assignments/')),
                ('marks', models.IntegerField(default=0)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assignment.assignment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
        ),
    ]
