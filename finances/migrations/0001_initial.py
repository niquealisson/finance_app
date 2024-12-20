# Generated by Django 5.0.7 on 2024-11-25 12:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Transacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('entrada', 'Entrada'), ('saida', 'Saída')], max_length=7)),
                ('descricao', models.CharField(max_length=255)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data', models.DateField()),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finances.categoria')),
            ],
        ),
    ]
