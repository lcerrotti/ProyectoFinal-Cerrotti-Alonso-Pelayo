# Generated by Django 3.2.8 on 2022-08-17 03:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RegistroUsuarios', '__first__'),
        ('Blog_General', '0013_comentario_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='imagen',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='RegistroUsuarios.avatar'),
        ),
    ]
