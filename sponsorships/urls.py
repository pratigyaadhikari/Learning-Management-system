from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register("sponsorships", SponsorshipModelViewset)
router.register("payments", PaymentModelViewSet)

urlpatterns = router.urls