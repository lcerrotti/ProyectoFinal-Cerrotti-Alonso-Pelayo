# Generated by Django 4.0.6 on 2022-07-30 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog_General', '0008_remove_entry_preview'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='muestra_superior',
            field=models.CharField(choices=[('si', 'Si'), ('no', 'No')], default='no', max_length=10),
        ),
    ]
