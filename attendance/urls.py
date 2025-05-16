"""
URL routing for the attendance app: registers viewset for Attendance.
"""
from rest_framework import routers
from .views import AttendanceViewSet

router = routers.DefaultRouter()
router.register(r'attendance', AttendanceViewSet)

urlpatterns = router.urls
