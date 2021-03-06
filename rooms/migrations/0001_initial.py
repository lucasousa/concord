# Generated by Django 4.0 on 2021-12-31 04:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50, verbose_name='Nome da sala')),
                ('every_one_send_message', models.BooleanField(default=True, verbose_name='Todos podem enviar mensagem ?')),
                ('type', models.CharField(max_length=10, verbose_name='Tipo')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Sala',
                'verbose_name_plural': 'Salas',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(blank=True, null=True, verbose_name='Texto da mensagem')),
                ('file', models.FileField(blank=True, max_length=254, null=True, upload_to='media/file', verbose_name='Arquivo')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.room', verbose_name='Sala')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.user', verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Mensagem',
                'verbose_name_plural': 'Mensagens',
                'ordering': ['-created_at'],
            },
        ),
    ]
