from rest_framework.routers import DefaultRouter   #Creates URLs automatically for every ModelViewSet.
from .views import *

router = DefaultRouter()

router.register("courses",CourseModelViewset)
router.register("enrollments",EnrollmentModelViewSet)
router.register("assessments", AssessmentModelViewSet)
router.register("submissions", SubmissionModelViewSet)

urlpatterns = router.urls  #Makes all generated URLs available to Django.
