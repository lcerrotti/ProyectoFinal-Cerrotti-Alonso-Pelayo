# Generated by Django 3.2.8 on 2022-08-01 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog_General', '0009_entry_muestra_superior'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='descripcion',
            field=models.TextField(default='Some String', max_length=150),
        ),
    ]