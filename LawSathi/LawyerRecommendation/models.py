from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
# Create your laywer models here.

#Laywaer address
class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    province =  models.CharField(max_length=99)
    district =  models.CharField(max_length=100)
    location =  models.CharField(max_length=100)

    def __str__(self):
            return f"Address-{self.user.username}"
    

#laywaer details
from django.db import models
from django.contrib.auth.models import User
from sklearn.preprocessing import MinMaxScaler
import numpy as np

from django.db import models
from django.contrib.auth.models import User
from sklearn.preprocessing import MinMaxScaler
import numpy as np

class LawyerDetails(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    experience = models.PositiveIntegerField(help_text="Years of experience")
    bar_license = models.CharField(max_length=100, unique=True)
    average_case_completion_days = models.PositiveIntegerField()
    permanent_address = models.CharField(max_length=255)
    office_address = models.OneToOneField(Address, related_name='office_address', on_delete=models.CASCADE)
    is_lawyer = models.BooleanField(default=True, editable=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    Rating = models.IntegerField(default=0)

    def get_model_name(self):
        return 'lawyerdetails'

    def calculate_experience_rating(self):
        experience = int(self.experience)  # Explicitly cast to integer
        print(f"Experience: {experience}")  # Debug statement
        if experience >= 28:
            return 5
        elif experience >= 20:
            return 4
        elif experience >= 10:
            return 3
        elif experience >= 5:
            return 2
        else:
            return 1

    def calculate_composite_score(self):
        experience_rating = self.calculate_experience_rating()
        avgDaysOfCompletion_normalized = self.normalize_avgDaysOfCompletion()
        composite_score = (0.5 * experience_rating + 
                           0.25 * (1 - avgDaysOfCompletion_normalized))
        return composite_score

    def normalize_avgDaysOfCompletion(self):
        all_lawyers = LawyerDetails.objects.all()
        if not all_lawyers.exists():
            return 0  # Return 0 or some other default value if no lawyers exist
        avg_days = np.array([lawyer.average_case_completion_days for lawyer in all_lawyers]).reshape(-1, 1)
        scaler = MinMaxScaler()
        scaler.fit(avg_days)
        normalized_value = scaler.transform(np.array([[self.average_case_completion_days]]))[0][0]
        return normalized_value
    
    def calculate_final_rating(self):
        composite_score = self.calculate_composite_score()
        print(f"Composite Score: {composite_score}")  # Debug statement
        if composite_score >= 2.5:
            return 5
        elif composite_score >= 2:
            return 4
        elif composite_score >= 1.5:
            return 3
        elif composite_score >= 1:
            return 2
        else:
            return 1

    def save(self, *args, **kwargs):
        self.Rating = self.calculate_final_rating()
        super(LawyerDetails, self).save(*args, **kwargs)
#lawyer documents
class LawyerDocuments(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    license_certificate = models.FileField(upload_to='documents/license_certificates/')
    citizenship_document = models.FileField(upload_to='documents/lcitizenship_document/')
    personal_photos = models.ImageField(upload_to='documents/personal_photos/')

    def __str__(self):
        return f"Dcouments of {self.user.username}"

class Lawyerdataset(models.Model):
    name = models.CharField(max_length=255)
    experience = models.IntegerField()
    average_case_completion_days = models.IntegerField()
    bar_license = models.CharField(max_length=255)
    rating = models.IntegerField()
    province = models.CharField(max_length=255)

    class Meta:
        db_table = 'lawyerrecommendation_lawyerdataset'
        
    def __str__(self):
        return self.name
    def get_model_name(self):
        return 'lawyerdataset'

@receiver(post_save, sender=LawyerDetails)
def accept_or_reject_email(sender, instance, created, **kwargs):
    # print(instance.user)
    if instance.status == 'rejected':
        subject = 'Sorry! Your form has been rejected'
        html_message = render_to_string('reject_emailtemplate.html', {'lawyer_name': instance.user.username})
        plain_message = strip_tags(html_message)
        from_email = 'your_email@gmail.com'  # Sender email address
        to_email = instance.user.email  # Lawyer's email address
        send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
        User.objects.get(username=instance.user).delete()
    if instance.status == 'approved':  # Check if status is 'approved'
        subject = 'Congratulations! Your form has been accepted'
        html_message = render_to_string('approved_emailtemplate.html', {'lawyer_name': instance.user.username})
        plain_message = strip_tags(html_message)
        from_email = 'your_email@gmail.com'  # Sender email address
        to_email = instance.user.email  # Lawyer's email address
        send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

# defining models for lawyer booking
class  Booking (models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    lawyer = models.ForeignKey(LawyerDetails, on_delete=models.CASCADE, related_name="bookings")
    date = models.DateField()
    time = models.TimeField()  # Add the time field
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')] ,default='Pending')
    meeting_link = models.URLField(blank=True, null=True)
    room_id = models.IntegerField(blank=True,null=True)
    class Meta:
        unique_together = ('lawyer', 'date', 'time')  # Ensure no double bookings

    def __str__(self):
        return f"{self.client.username} booked {self.lawyer.user.username} on {self.date} at {self.time}"

