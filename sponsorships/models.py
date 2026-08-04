from django.db import models
from accounts.models import SponsorProfile
from courses.models import Course

# Create your models here.

# Sponsorship Model
class Sponsorship(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACTIVE = "ACTIVE", "Active"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    sponsor = models.ForeignKey(SponsorProfile,on_delete=models.CASCADE,related_name="sponsorships")
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="sponsorships")
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.PENDING)
    start_date = models.DateField()
    end_date = models.DateField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sponsor.company_name} - {self.course.title}"


# Payment Model
class Payment(models.Model):

    class PaymentMethod(models.TextChoices):
        BANK = "BANK", "Bank Transfer"
        ESEWA = "ESEWA", "eSewa"
        KHALTI = "KHALTI", "Khalti"
        CASH = "CASH", "Cash"

    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        FAILED = "FAILED", "Failed"

    sponsorship = models.ForeignKey(Sponsorship,on_delete=models.CASCADE,related_name="payments")
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    payment_method = models.CharField(max_length=20,choices=PaymentMethod.choices)
    transaction_id = models.CharField(max_length=100,unique=True)
    payment_status = models.CharField(max_length=20,choices=PaymentStatus.choices,default=PaymentStatus.PENDING)
    paid_at = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.transaction_id