# Generated by Django 4.2.10 on 2024-03-10 00:30

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('externaluser', '0010_plano_alter_perfil_plano'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fatura_gerada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_fatura', models.CharField(choices=[('1', 'GERADA'), ('2', 'EM ATRASO'), ('3', 'PAGA')], max_length=50, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('cliente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='perfil', to='externaluser.perfil')),
            ],
        ),
    ]
