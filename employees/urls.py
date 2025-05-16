"""
URL routing for the employees app: registers viewsets for Department, Employee, and Performance.
"""
from rest_framework import routers
from .views import DepartmentViewSet, EmployeeViewSet, PerformanceViewSet
from django.urls import path
from .views import (
    charts_view, employees_per_department,
    monthly_attendance_summary, department_list
)

router = routers.DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'performances', PerformanceViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('charts/', charts_view),
    path('charts/employees-per-department/', employees_per_department),
    path('charts/monthly-attendance/', monthly_attendance_summary),
    path('charts/departments/', department_list)
]