# Generated by Django 4.0.5 on 2022-09-07 00:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mercado', '0013_alter_layout_usuario_alter_material_dureza'),
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
            field=models.CharField(choices=[('blando', 'Blando'), ('duro', 'Duro'), ('medio', 'Medio')], max_length=20),
        ),
    ]
