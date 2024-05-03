# Generated by Django 5.0.1 on 2024-03-28 16:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_donormodel_options_donation_date_time_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInputGenai',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_message', models.TextField()),
                ('document', models.FileField(blank=True, null=True, upload_to='documents/')),
                ('bot_message', models.TextField(blank=True, null=True, verbose_name='Message')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
