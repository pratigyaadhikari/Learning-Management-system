from django.db import models
from django.conf import settings

# Create your models here.

class Notification(models.Model):

    class NotificationType(models.TextChoices):
        NEW_ASSESSMENT = "NEW_ASSESSMENT", "New Assessment"
        ASSESSMENT_DUE = "ASSESSMENT_DUE", "Assessment Due"
        ASSESSMENT_RESULT = "ASSESSMENT_RESULT", "Assessment Result"
        COURSE_PROGRESS = "COURSE_PROGRESS", "Course Progress"
        NEW_SUBMISSION = "NEW_SUBMISSION", "New Submission"

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    title = models.CharField(max_length=200)

    message = models.TextField()

    notification_type = models.CharField(
        max_length=30,
        choices=NotificationType.choices
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recipient.username} - {self.title}"