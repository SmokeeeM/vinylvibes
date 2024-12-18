# Generated by Django 5.1.1 on 2024-12-03 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('descripcion', models.TextField()),
                ('precio', models.DecimalField(decimal_places=3, max_digits=6)),
                ('imagen', models.ImageField(upload_to='media/')),
                ('stock', models.PositiveIntegerField()),
                ('artista', models.CharField(max_length=45)),
            ],
        ),
    ]
