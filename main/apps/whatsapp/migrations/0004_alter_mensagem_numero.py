# Generated by Django 4.2.10 on 2025-03-03 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whatsapp', '0003_mensagem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensagem',
            name='numero',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
