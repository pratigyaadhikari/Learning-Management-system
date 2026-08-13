from django.urls import path
from .views import AdminDashboardView,SponsorDashboardView

urlpatterns = [
    path("admin/", AdminDashboardView.as_view(), name="admin-dashboard"),
    path("sponsor/",SponsorDashboardView.as_view(),name="sponsor-dashboard"
),
]
