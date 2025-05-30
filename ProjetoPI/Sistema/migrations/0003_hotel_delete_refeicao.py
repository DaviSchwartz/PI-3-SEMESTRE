# Generated by Django 5.2.1 on 2025-05-29 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema', '0002_profile_alter_restaurante_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome do Hotel')),
                ('cnpj', models.CharField(max_length=18, unique=True, verbose_name='CNPJ')),
                ('cidade', models.CharField(max_length=18, unique=True, verbose_name='Cidade')),
                ('endereco', models.TextField(verbose_name='Endereço Completo')),
                ('telefone', models.CharField(max_length=15, verbose_name='Telefone')),
                ('responsavel', models.CharField(max_length=100, verbose_name='Responsável')),
            ],
        ),
        migrations.DeleteModel(
            name='Refeicao',
        ),
    ]
