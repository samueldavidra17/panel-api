# Generated by Django 4.1.2 on 2022-11-30 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='impresoras',
            name='tipo_impresion',
        ),
        migrations.AlterField(
            model_name='impresoras',
            name='csb',
            field=models.CharField(default='S/N', max_length=45),
        ),
        migrations.AlterField(
            model_name='impresoras',
            name='ip',
            field=models.CharField(default='No aplica', max_length=45),
        ),
        migrations.AlterField(
            model_name='impresoras',
            name='serial',
            field=models.CharField(default='S/N', max_length=45),
        ),
    ]
