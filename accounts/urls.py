from django.urls import path

from rest_framework.routers import DefaultRouter
from .views import UserModelViewSet, StudentProfileModelViewSet,InstructorProfileModelViewSet,SponsorProfileModelViewSet, LoginView

router = DefaultRouter()

router.register("users", UserModelViewSet)
router.register("students", StudentProfileModelViewSet)
router.register("instructors", InstructorProfileModelViewSet)
router.register("sponsors", SponsorProfileModelViewSet)

urlpatterns =[
    path("login/", LoginView.as_view(), name="login"),
    ] + router.urls