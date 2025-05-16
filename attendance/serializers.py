"""
Serializer for Attendance records.
"""
from rest_framework import serializers
from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    """Serializer for Attendance entries."""
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=__import__('employees').models.Employee.objects.all(),
        source='employee',
        write_only=True,
        help_text="ID of the employee"
    )
    employee = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'employee', 'employee_id', 'date', 'status']
