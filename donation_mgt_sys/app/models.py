from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image


# Create your models here.
class BlogModel(models.Model):
    image = models.ImageField(upload_to='blog_images/', verbose_name='Blog Image')
    title = models.CharField(max_length=150, verbose_name='Title')
    about = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title


class AboutModel(models.Model):
    image = models.ImageField(upload_to='about_images/', verbose_name='About Image')
    name = models.CharField(max_length=150, verbose_name='Name')
    description = models.TextField()
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class ServiceModel(models.Model):
    image = models.ImageField(upload_to='service_images/', verbose_name='Service Image')
    title = models.CharField(max_length=150, verbose_name='Title')
    description = models.TextField()
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title


class FeedbackModel(models.Model):
    image = models.ImageField(upload_to='feedback_images/', verbose_name='Feedback Image')
    name = models.CharField(max_length=150, verbose_name='Name')
    feedback = models.TextField()
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class EventsModel(models.Model):
    image = models.ImageField(upload_to='event_images/', verbose_name='Event Image')
    title = models.CharField(max_length=150, verbose_name='Title')
    description = models.TextField()
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title


class GalleryModel(models.Model):
    image = models.ImageField(upload_to='gallery_images/', verbose_name='Gallery Image')
    title = models.CharField(max_length=150, verbose_name='Title')
    about = models.TextField()
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title


class TeamModel(models.Model):
    image = models.ImageField(upload_to='team_images/', verbose_name='Team Image')
    name = models.CharField(max_length=150, verbose_name='Name')
    post = models.CharField(max_length=150, verbose_name='Post Name')
    description = models.TextField()
    twitter = models.CharField(max_length=150, verbose_name='Twitter', null=True, blank=True)
    facebook = models.CharField(max_length=150, verbose_name='Facebook', null=True, blank=True)
    gmail = models.CharField(max_length=150, verbose_name='Gmail', null=True, blank=True)
    linkdin = models.CharField(max_length=150, verbose_name='Linkdin', null=True, blank=True)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class ContactModel(models.Model):
    name = models.CharField(max_length=150, verbose_name='Name')
    email = models.EmailField(verbose_name='Email Id')
    message = models.TextField()
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class SubscriptionModel(models.Model):
    email = models.EmailField(verbose_name='Email Id')
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.email


class MyUser(AbstractUser):
    REGISTRATION_CHOICES = [
        ('Is Volunteers', 'Is Volunteers'),
        ('Is Donor', 'Is Donor'),
    ]
    type = models.CharField(max_length=20, choices=REGISTRATION_CHOICES)
    is_completed = models.BooleanField(default=False)


class DonorModel(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='donor_user')
    profile_image = models.ImageField(upload_to='profile_images/', verbose_name='Profile Image', default='default_profile.png')
    name = models.CharField(max_length=100, verbose_name='Full Name')
    email = models.EmailField(verbose_name='Email Id', unique=True)
    mobile_number = models.BigIntegerField(verbose_name='Mobile Number')
    id_proof = models.FileField(upload_to='resumes/', verbose_name='Aadhaar Card')
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Donor Model'
        verbose_name_plural = 'Donor Model'
        permissions = [
            ("can_view_donors_custom", "Can View Job Donors Custom"),
        ]


class VolunteerModel(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='donation_recruiter')
    company_image = models.ImageField(upload_to='company_images/', verbose_name='Company Image')
    company_name = models.CharField(max_length=100, verbose_name='Company Full Name')
    lic_no = models.CharField(max_length=15, verbose_name='Licence Number')
    lic_doc = models.FileField(upload_to='gst_documents/', verbose_name='Upload Licence Proof')
    email_id = models.EmailField(verbose_name='Email Id', unique=True)
    mobile_number = models.BigIntegerField(verbose_name='Mobile Number')
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = 'Volunteer'
        verbose_name_plural = 'Volunteers'
        permissions = [
            ("can_view_volunteer_custom", "Can View Volunteer Custom"),
        ]


class Donation(models.Model):
    DONATION_TYPE_CHOICES = (
        ('money', 'Money'),
        ('goods', 'Goods'),
        ('time', 'Time'),
        ('food', 'Food'),
        ('clothing', 'Clothing'),
        ('books', 'Books'),
        ('toys', 'Toys'),
        ('electronics', 'Electronics'),
        ('furniture', 'Furniture'),
        ('medical_supplies', 'Medical Supplies'),
        ('vehicles', 'Vehicles'),
        ('appliances', 'Appliances'),
        ('artwork', 'Artwork'),
        ('sports_equipment', 'Sports Equipment'),
        ('tools', 'Tools'),
    )
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    applicants = models.ManyToManyField(VolunteerModel, related_name="applied_donation", blank=True)
    recuiter = models.ForeignKey(DonorModel, related_name='volunteer', null=True, on_delete=models.CASCADE)
    donation_title = models.CharField(max_length=100)
    donation_description = models.TextField()
    company_name = models.CharField(max_length=100)
    company_image = models.ImageField(upload_to='company_images/', verbose_name='Company Image', null=True)
    donation_location = models.CharField(max_length=100)
    donation_type = models.CharField(max_length=20, choices=DONATION_TYPE_CHOICES)
    contact_information = models.CharField(max_length=100)
    date_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.donation_title


class UserInputGenai(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    user_message = models.TextField()
    document = models.FileField(upload_to='documents/', null=True, blank=True)
    bot_message = models.TextField(verbose_name="Message", null=True, blank=True)

    def __str__(self):
        return self.user_message