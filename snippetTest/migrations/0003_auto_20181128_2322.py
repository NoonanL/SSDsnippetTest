# Generated by Django 2.1 on 2018-11-28 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippetTest', '0002_snippet'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='language',
            field=models.TextField(default='java'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='snippet',
            name='title',
            field=models.TextField(default='my code'),
            preserve_default=False,
        ),
    ]
