# Generated by Django 4.2.10 on 2024-03-09 23:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('externaluser', '0009_alter_perfil_plano_delete_plano'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plano',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plano', models.CharField(max_length=40, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('status', models.CharField(choices=[('1', 'ATIVO'), ('2', 'INATIVO')], max_length=40, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='perfil',
            name='plano',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='externaluser.plano'),
        ),
    ]
