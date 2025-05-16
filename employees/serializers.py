"""
Serializers for Employee domain models.
Handles validation and conversion between model instances and JSON payloads.
"""
from rest_framework import serializers
from .models import Department, Employee, Performance


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department objects."""
    class Meta:
        model = Department
        fields = ['id', 'name']


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for Employee objects, including nested department name."""
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        source='department',
        write_only=True,
        help_text="ID of the department the employee belongs to"
    )

    class Meta:
        model = Employee
        fields = [
            'id', 'name', 'email', 'phone_number',
            'address', 'date_of_joining',
            'department', 'department_id'
        ]


class PerformanceSerializer(serializers.ModelSerializer):
    """Serializer for Performance reviews."""
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        source='employee',
        write_only=True,
        help_text="ID of the employee being reviewed"
    )
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = Performance
        fields = ['id', 'employee', 'employee_id', 'rating', 'review_date']

