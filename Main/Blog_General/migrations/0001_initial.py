# Generated by Django 3.2.8 on 2022-07-27 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('contenido', models.CharField(max_length=1000)),
                ('imagen', models.URLField()),
                ('autor', models.CharField(max_length=100)),
                ('fecha', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
