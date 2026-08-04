from django.contrib import admin
from .models import Sponsorship, Payment

# Register your models here.

@admin.register(Sponsorship)
class SponsorshipAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "sponsor",
        "course",
        "amount",
        "status",
        "start_date",
        "end_date",
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "sponsorship",
        "amount",
        "payment_method",
        "payment_status",
        "paid_at",
    )