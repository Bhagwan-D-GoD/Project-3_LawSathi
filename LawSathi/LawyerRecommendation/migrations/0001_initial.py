# Generated by Django 5.0.7 on 2024-08-20 16:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('province', models.CharField(max_length=99)),
                ('district', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='LawyerDocuments',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('license_certificate', models.FileField(upload_to='documents/license_certificates/')),
                ('citizenship_document', models.FileField(upload_to='documents/lcitizenship_document/')),
                ('personal_photos', models.ImageField(upload_to='documents/personal_photos/')),
            ],
        ),
        migrations.CreateModel(
            name='LawyerDetails',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('experience', models.PositiveIntegerField(help_text='Years of experience')),
                ('bar_license', models.CharField(max_length=100, unique=True)),
                ('average_case_completion_days', models.PositiveIntegerField()),
                ('permanent_address', models.CharField(max_length=255)),
                ('is_lawyer', models.BooleanField(default=True, editable=False)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('Rating', models.IntegerField(default=0)),
                ('office_address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='office_address', to='LawyerRecommendation.address')),
            ],
        ),
    ]
