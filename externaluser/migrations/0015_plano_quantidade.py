# Generated by Django 4.2.10 on 2024-03-13 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('externaluser', '0014_perfil_cpf_or_cnpj_alter_perfil_cpf_cnpj_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='plano',
            name='quantidade',
            field=models.IntegerField(null=True),
        ),
    ]
