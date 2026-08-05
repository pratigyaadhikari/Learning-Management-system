from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        INSTRUCTOR = 'INSTRUCTOR', 'Instructor'
        STUDENT = 'STUDENT', 'Student'
        SPONSOR = 'SPONSOR', 'Sponsor'
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.STUDENT)
    # ROLES=[("ADMIN","Admin"),("INSTRUCTOR","Instructor"),("STUDENT","Student"),("SPONSOR","Sponsor")]
    # role = models.CharField(max_length=20, choices=ROLES, default="STUDENT")
    def __str__(self):
        return self.username
    
    
class StudentProfile(models.Model):
    user =models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    interests = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Student Profile"
    
class InstructorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructor_profile')
    bio = models.TextField(blank=True)
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Instructor Profile: {self.user.username}"
    
class SponsorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="sponsor_profile")
    company_name = models.CharField(max_length=100)
    company_website = models.URLField(blank=True)
    
    def __str__(self):
        return f"Sponsor Profile: {self.company_name}"    