from django.db import models
from accounts.models import InstructorProfile
# Create your models here.
class Course(models.Model):
    class Difficulty(models.TextChoices):
        BEGINNER = "BEGINNER","Beginner"
        INTERMEDIATE = "INTERMEDIATE","Intermediate"
        ADVANCED = "ADVANCED","Advanced"
        
    difficulty = models.CharField(max_length=50, choices=Difficulty.choices, default=Difficulty.BEGINNER)    
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE, related_name="courses_taught") 
    price = models.DecimalField(max_digits=8,decimal_places=2, default=0.00) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title