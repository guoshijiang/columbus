# Generated by Django 2.2.7 on 2021-09-24 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('name', models.CharField(default='admin', max_length=100, verbose_name='用户名')),
                ('password', models.CharField(default='', max_length=100, verbose_name='密码')),
                ('token', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='token')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否是有效')),
            ],
            options={
                'verbose_name': '用户表',
                'verbose_name_plural': '用户表',
            },
        ),
    ]
