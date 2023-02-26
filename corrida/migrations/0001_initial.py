# Generated by Django 4.1.6 on 2023-02-26 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Corrida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ano', models.IntegerField()),
                ('fechaLimite', models.DateField()),
            ],
            options={
                'verbose_name': 'corrida',
                'verbose_name_plural': 'corridas',
            },
        ),
    ]