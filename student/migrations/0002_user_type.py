# Generated by Django 4.0.8 on 2023-10-05 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.CharField(default='student', editable=False, max_length=7),
        ),
    ]
