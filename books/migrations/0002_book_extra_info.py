# Generated by Django 4.1.7 on 2023-11-21 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='extra_info',
            field=models.JSONField(default=None, null=True),
        ),
    ]
