# Generated by Django 3.2.8 on 2022-07-25 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RegistroUsuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preferencias_Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lenguaje', models.CharField(max_length=40)),
                ('backOfront', models.CharField(max_length=40)),
                ('pais', models.CharField(max_length=40)),
                ('trabajo', models.CharField(max_length=40)),
            ],
        ),
    ]