from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from courses.models import Assessment
from courses.emails import send_assessment_deadline_reminders

from notifications.utils import notify_assessment_due


class Command(BaseCommand):
    help = "Send reminder emails for assessments due soon."

    def handle(self, *args, **options):
        now = timezone.now()
        reminder_limit = now + timedelta(days=2)

        assessments = Assessment.objects.filter(
            due_date__isnull=False,
            due_date__gte=now,
            due_date__lte=reminder_limit,
        )

        count = 0

        for assessment in assessments:
            send_assessment_deadline_reminders(assessment)

            students = assessment.course.enrollments.filter(
                status="ACTIVE"
            ).select_related("student__user")

            notify_assessment_due(
                assessment,
                [enrollment.student for enrollment in students]
            )

            count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Deadline reminders processed for {count} assessment(s)."
            )
        )