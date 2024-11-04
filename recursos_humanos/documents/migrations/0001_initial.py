# Generated by Django 5.1.2 on 2024-11-02 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(help_text='Nombre o título del documento', max_length=200, unique=True)),
                ('description', models.TextField(help_text='Descripción del documento')),
                ('file', models.FileField(help_text='Archivo del documento', upload_to='documents/')),
                ('is_ready', models.BooleanField(default=False, help_text='Indica si el archivo está listo después del análisis')),
            ],
            options={
                'verbose_name': 'document',
                'verbose_name_plural': 'documents',
            },
        ),
    ]
