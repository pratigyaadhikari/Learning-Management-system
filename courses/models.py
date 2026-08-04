from django.db import models
from accounts.models import InstructorProfile, StudentProfile

# Course Model
class Course(models.Model):

    class Difficulty(models.TextChoices):
        BEGINNER = "BEGINNER", "Beginner"
        INTERMEDIATE = "INTERMEDIATE", "Intermediate"
        ADVANCED = "ADVANCED", "Advanced"

    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(InstructorProfile,on_delete=models.CASCADE,related_name="courses_taught")
    difficulty = models.CharField(max_length=20,choices=Difficulty.choices,default=Difficulty.BEGINNER)
    price = models.DecimalField(max_digits=8,decimal_places=2,default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# Enrollment Model
class Enrollment(models.Model):

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        COMPLETED = "COMPLETED", "Completed"
        DROPPED = "DROPPED", "Dropped"

    student = models.ForeignKey(StudentProfile,on_delete=models.CASCADE,related_name="enrollments")
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="enrollments")
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.ACTIVE)
    progress_percent = models.PositiveSmallIntegerField(default=0)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True,null=True)

    class Meta:
        # Stops the same student from enrolling in the same course twice.
        # PostgreSQL will enforce this at the database level too.
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student.user.username} - {self.course.title}"


# Assessment Model
class Assessment(models.Model):

    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="assessments")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(blank=True,null=True)
    max_score = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.course.title})"


# Submission Model
class Submission(models.Model):

    assessment = models.ForeignKey(Assessment,on_delete=models.CASCADE,related_name="submissions")
    student = models.ForeignKey(StudentProfile,on_delete=models.CASCADE,related_name="submissions")
    submitted_file = models.FileField( upload_to="submissions/",blank=True,null=True)
    score = models.PositiveIntegerField(blank=True,null=True)
    feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("assessment", "student")

    def __str__(self):
        return f"{self.student.user.username} - {self.assessment.title}"