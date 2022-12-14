# Generated by Django 4.0.5 on 2022-09-07 00:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mercado', '0015_alter_layout_primeretapa_alter_layout_segundaetapa_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layout',
            name='primerEtapa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primerEtapa', to='mercado.patrimonio'),
        ),
        migrations.AlterField(
            model_name='layout',
            name='segundaEtapa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='segundaEtapa', to='mercado.patrimonio'),
        ),
        migrations.AlterField(
            model_name='material',
            name='dureza',
            field=models.CharField(choices=[('blando', 'Blando'), ('medio', 'Medio'), ('duro', 'Duro')], max_length=20),
        ),
    ]
