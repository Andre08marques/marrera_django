# Generated by Django 4.2.10 on 2024-03-09 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('externaluser', '0005_perfil_cobrefacil_id_perfil_vencimento'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
