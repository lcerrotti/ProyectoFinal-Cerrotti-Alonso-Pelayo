# Generated by Django 4.0.6 on 2022-08-01 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_juegos', '0003_alter_juegos_descripcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='juegos',
            name='urlimagen',
            field=models.CharField(max_length=200),
        ),
    ]