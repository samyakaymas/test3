# Generated by Django 3.0.7 on 2020-06-18 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200618_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='can_edit_theory',
            field=models.BooleanField(default=True),
        ),
    ]
