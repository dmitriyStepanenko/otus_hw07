# Generated by Django 3.2.8 on 2021-10-28 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='header',
            field=models.CharField(default='aa', max_length=200),
            preserve_default=False,
        ),
    ]
