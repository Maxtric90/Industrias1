# Generated by Django 4.0.6 on 2022-08-07 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Industrias1App', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='dinero',
            field=models.IntegerField(default=10000),
            preserve_default=False,
        ),
    ]
