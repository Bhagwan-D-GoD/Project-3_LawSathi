# Generated by Django 5.0.7 on 2024-08-20 07:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "LawyerRecommendation",
            "0004_alter_lawyerdocuments_citizenship_document_and_more",
        ),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="FileUpload",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.FileField(upload_to="documents/law_pdfs")),
                ("name", models.CharField(max_length=255)),
                ("uploaded_date", models.DateTimeField(auto_now_add=True)),
                ("description", models.CharField(blank=True, max_length=255)),
                (
                    "uploaded_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
