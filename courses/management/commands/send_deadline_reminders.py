from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from courses.models import Assessment
from courses.emails import send_assessment_deadline_reminders


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
            count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Deadline reminders processed for {count} assessment(s)."
            )
        )