"""
ViewSet for Attendance records.
"""
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Attendance
from .serializers import AttendanceSerializer
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(tags=['Departments'])
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related('employee').all()
    serializer_class = AttendanceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['employee__id', 'date', 'status']
