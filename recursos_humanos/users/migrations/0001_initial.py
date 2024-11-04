# Generated by Django 5.1.2 on 2024-11-02 05:59

import django.db.models.deletion
import recursos_humanos.users.custom_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=50, unique=True)),
                ('middle_name', models.CharField(max_length=50, unique=True)),
                ('last_name', models.CharField(max_length=50, unique=True)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('contract_type', models.CharField(blank=True, max_length=20, null=True)),
                ('base_salary', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('vacation_days', models.IntegerField(blank=True, null=True)),
                ('job_title', models.CharField(max_length=50)),
                ('department', models.CharField(max_length=50)),
                ('plant', models.CharField(max_length=50)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='ConversationThreadModel',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', recursos_humanos.users.custom_fields.UUIDPrimaryKeyField(editable=False, max_length=32, null=False, primary_key=True, serialize=False, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'conversation thread',
                'verbose_name_plural': 'conversation threads',
            },
        ),
        migrations.CreateModel(
            name='ConversationMessageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('role', models.CharField(choices=[('system', 'SYSTEM'), ('user', 'USER'), ('assistant', 'ASSISTANT')], max_length=20)),
                ('message', models.TextField()),
                ('conversation_thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.conversationthreadmodel')),
            ],
            options={
                'verbose_name': 'conversation message',
                'verbose_name_plural': 'conversation messages',
            },
        ),
        migrations.AddIndex(
            model_name='usermodel',
            index=models.Index(fields=['id'], name='user_id_idx'),
        ),
        migrations.AddIndex(
            model_name='conversationthreadmodel',
            index=models.Index(fields=['id'], name='conversation_thread_id_idx'),
        ),
        migrations.AddIndex(
            model_name='conversationmessagemodel',
            index=models.Index(fields=['id'], name='conversation_message_id_idx'),
        ),
    ]
