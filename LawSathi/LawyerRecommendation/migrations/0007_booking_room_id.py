# Generated by Django 5.0.7 on 2024-08-23 05:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("LawyerRecommendation", "0006_booking_meeting_link"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="room_id",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
