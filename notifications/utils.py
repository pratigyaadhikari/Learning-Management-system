from .models import Notification


def notify_new_assessment(assessment, students):
    for student in students:
        Notification.objects.create(
            recipient=student.user,
            title="New Assessment",
            message=(
                f"A new assessment '{assessment.title}' has been added "
                f"to the course '{assessment.course.title}'."
            ),
            notification_type=Notification.NotificationType.NEW_ASSESSMENT,
        )
        
def notify_assessment_due(assessment, students):
    for student in students:
        exists = Notification.objects.filter(
            recipient=student.user,
            notification_type=Notification.NotificationType.ASSESSMENT_DUE,
            message__contains=assessment.title,
        ).exists()

        if exists:
            continue

        Notification.objects.create(
            recipient=student.user,
            title="Assessment Due Soon",
            message=(
                f"Your assessment '{assessment.title}' for "
                f"'{assessment.course.title}' is due on "
                f"{assessment.due_date}."
            ),
            notification_type=Notification.NotificationType.ASSESSMENT_DUE,
        )
        
def notify_instructor_course_progress(course):
    instructor = course.instructor.user

    enrollments = course.enrollments.all()

    total_students = enrollments.count()

    if total_students == 0:
        return

    completed_students = enrollments.filter(
        status="COMPLETED"
    ).count()

    average_progress = sum(
        enrollment.progress_percent
        for enrollment in enrollments
    ) / total_students

    completion_rate = (
        completed_students / total_students
    ) * 100

    Notification.objects.create(
        recipient=instructor,
        title="Course Progress Update",
        message=(
            f"Course '{course.title}' has {total_students} enrolled "
            f"student(s). {completed_students} student(s) have completed "
            f"the course. Completion rate: {completion_rate:.1f}%. "
            f"Average student progress: {average_progress:.1f}%."
        ),
        notification_type=Notification.NotificationType.COURSE_PROGRESS,
    )
    
def notify_assessment_result(submission):
    student = submission.student.user
    assessment = submission.assessment

    Notification.objects.create(
        recipient=student,
        title="Assessment Result",
        message=(
            f"Your result for '{assessment.title}' in "
            f"'{assessment.course.title}' is available. "
            f"Score: {submission.score}. "
            f"Feedback: {submission.feedback or 'No feedback provided.'}"
        ),
        notification_type=Notification.NotificationType.ASSESSMENT_RESULT,
    )
    
    
def notify_instructor_new_submission(submission):
    instructor = submission.assessment.course.instructor.user
    student = submission.student.user
    assessment = submission.assessment
    course = assessment.course

    Notification.objects.create(
        recipient=instructor,
        title="New Submission",
        message=(
            f"{student.username} has submitted the assessment "
            f"'{assessment.title}' for your course '{course.title}'."
        ),
        notification_type=Notification.NotificationType.NEW_SUBMISSION,
    )