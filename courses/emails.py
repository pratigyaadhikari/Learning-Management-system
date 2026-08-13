from django.core.mail import send_mail
from django.conf import settings


def send_assessment_result_email(
    student_email,
    student_name,
    assessment_title,
    course_title,
    score,
    feedback,
):
    subject = f"Assessment Result - {assessment_title}"

    message = f"""
Hello {student_name},

Your assessment result is now available.

Course: {course_title}
Assessment: {assessment_title}
Score: {score}

Feedback:
{feedback or "No feedback provided."}

Thank you,
Learning Management System
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [student_email],
        fail_silently=False,
    )
    
def send_deadline_reminder_email(
    student_email,
    student_name,
    assessment_title,
    course_title,
    due_date,
):
    subject = f"Deadline Reminder - {assessment_title}"

    message = f"""
Hello {student_name},

This is a reminder that your assessment is approaching its deadline.

Course: {course_title}
Assessment: {assessment_title}
Due Date: {due_date}

Please make sure to submit your assessment before the deadline.

Thank you,
Learning Management System
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [student_email],
        fail_silently=False,
    )
    
def send_progress_report_email(
    sponsor_email,
    sponsor_name,
    student_name,
    course_title,
    progress_percent,
):
    subject = f"Student Progress Report - {student_name}"

    message = f"""
Hello {sponsor_name},

Here is the latest progress report for the student you are sponsoring.

Student: {student_name}
Course: {course_title}
Progress: {progress_percent}%

Thank you for supporting the student's learning journey.

Learning Management System
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [sponsor_email],
        fail_silently=False,
    )
    
    
def send_sponsor_progress_report(sponsorship):
    sponsor = sponsorship.sponsor
    student = sponsorship.student
    course = sponsorship.course

    if not student:
        return

    enrollment = student.enrollments.filter(
        course=course
    ).first()

    if not enrollment:
        return

    sponsor_user = sponsor.user
    student_user = student.user

    send_progress_report_email(
        sponsor_email=sponsor_user.email,
        sponsor_name=sponsor.company_name,
        student_name=student_user.username,
        course_title=course.title,
        progress_percent=enrollment.progress_percent,
    )
    
    
def send_assessment_deadline_reminders(assessment):
    if not assessment.due_date:
        return

    enrollments = assessment.course.enrollments.filter(
        status="ACTIVE"
    ).select_related("student__user")

    for enrollment in enrollments:
        student = enrollment.student
        student_user = student.user

        if not student_user.email:
            continue

        send_deadline_reminder_email(
            student_email=student_user.email,
            student_name=student_user.username,
            assessment_title=assessment.title,
            course_title=assessment.course.title,
            due_date=assessment.due_date,
        )