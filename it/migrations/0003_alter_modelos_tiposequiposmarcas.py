# Generated by Django 4.1.2 on 2023-01-16 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0002_alter_departamentosempresas_table_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelos',
            name='tiposEquiposMarcas',
            field=models.ForeignKey(null='True', on_delete=django.db.models.deletion.CASCADE, related_name='tiposEquiposMarcasId', to='it.tiposequiposmarcas'),
        ),
    ]
