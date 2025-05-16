# employees/views.py
from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncMonth
from rest_framework import viewsets, filters, pagination, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
from django.utils.timezone import now
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import logging

from .models import Department, Employee, Performance
from .serializers import DepartmentSerializer, EmployeeSerializer, PerformanceSerializer
from attendance.models import Attendance


# ----------------------
# Logging Setup
# ----------------------
logger = logging.getLogger(__name__)
handler = logging.FileHandler('user_registration.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


# ----------------------
# Cursor-Based Pagination Class
# ----------------------

class CursorResultsSetPagination(pagination.CursorPagination):
    page_size = 10
    ordering = '-id'


# ----------------------
# Role-Based Permissions
# ----------------------

def is_hr(user):
    return user.groups.filter(name='HR').exists()

def is_employee(user):
    return user.groups.filter(name='Employee').exists()


# ----------------------
# ViewSets (with role-based access + cursor pagination)
# ----------------------

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = CursorResultsSetPagination
    permission_classes = [IsAuthenticated]


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related('department').all()
    serializer_class = EmployeeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['department__id', 'date_of_joining']
    search_fields = ['name', 'email']
    ordering_fields = ['name', 'date_of_joining']
    pagination_class = CursorResultsSetPagination

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related('employee').all()
    serializer_class = PerformanceSerializer
    pagination_class = CursorResultsSetPagination
    permission_classes = [IsAuthenticated]


# ----------------------
# Charts Template View
# ----------------------

def charts_view(request):
    return render(request, 'charts.html')


    

# ----------------------
# API: Employees Per Department (w/ total summary)
# ----------------------

@swagger_auto_schema(
    method='get',
    operation_description="Returns count of employees grouped by department with total",
    tags=['Charts'],
    responses={200: openapi.Response('JSON with labels, counts, and total')}
)

@api_view(['GET'])
@permission_classes([AllowAny]) 
def employees_per_department(request):

    data = (
        Department.objects
        .annotate(employee_count=Count('employees'))
        .values_list('name', 'employee_count')
    )
    labels = [name for name, _ in data]
    counts = [count for _, count in data]
    total = sum(counts)
    return Response({'labels': labels, 'counts': counts, 'total': total})


# ----------------------
# API: Monthly Attendance Overview (Chart)
# ----------------------

@swagger_auto_schema(
    method='get',
    operation_description="Returns monthly attendance summary, optional department filter.",
    tags=['Charts'],
    manual_parameters=[
        openapi.Parameter(
            'department_id',
            openapi.IN_QUERY,
            description="Filter by department",
            type=openapi.TYPE_INTEGER
        )
    ],
    responses={200: openapi.Response('JSON with present, absent, late counts')}
)
@api_view(['GET'])
@permission_classes([AllowAny]) 
def monthly_attendance_summary(request):
    user = request.user
    department_id = request.GET.get('department_id')

    queryset = Attendance.objects.select_related('employee')
    if is_employee(user):
        queryset = queryset.filter(employee__user=user)
    elif department_id:
        queryset = queryset.filter(employee__department_id=department_id)

    data = (
        queryset
        .annotate(month=TruncMonth('date'))
        .values('month', 'status')
        .order_by('month')
    )

    from collections import defaultdict
    summary = defaultdict(lambda: {'P': 0, 'A': 0, 'L': 0})
    for record in data:
        month = record['month'].strftime('%b %Y')
        summary[month][record['status']] += 1

    labels = list(summary.keys())
    present = [summary[m]['P'] for m in labels]
    absent = [summary[m]['A'] for m in labels]
    late = [summary[m]['L'] for m in labels]

    return Response({
        'labels': labels,
        'present': present,
        'absent': absent,
        'late': late
    })


# ----------------------
# API: Department Dropdown List
# ----------------------

@swagger_auto_schema(
    method='get',
    operation_description="Returns department ID and name list.",
    tags=['Charts'],
    responses={200: openapi.Response('List of departments')}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def department_list(request):
    departments = Department.objects.values_list('id', 'name')
    return Response([{'id': id_, 'name': name} for id_, name in departments])


# ----------------------
# API: Current Authenticated User Info
# ----------------------

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_staff': user.is_staff
    })


# ----------------------
# API: Register HR, Employee, or Admin (Admins can create Admins only)
# ----------------------

@swagger_auto_schema(
    method='post',
    operation_description="Registers a new user with role 'HR', 'Employee', or 'Admin'. Only admins can create Admins.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password', 'role'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'role': openapi.Schema(type=openapi.TYPE_STRING, enum=['Admin', 'HR', 'Employee'])
        },
    ),
    tags=['Authentication'],
    responses={201: openapi.Response('User registered successfully')}
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def register_user(request):
    data = request.data
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    role = data.get("role")  # 'HR', 'Employee', or 'Admin'

    if role not in ['HR', 'Employee', 'Admin']:
        return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

    if role == 'Admin' and not request.user.is_superuser:
        return Response({"error": "Only superusers can create Admins."}, status=status.HTTP_403_FORBIDDEN)

    if not Group.objects.filter(name=role).exists():
        Group.objects.create(name=role)

    user = User.objects.create_user(username=username, password=password, email=email)
    user.groups.add(Group.objects.get(name=role))

    if role == 'Admin':
        user.is_staff = True
        user.is_superuser = False  # Prevent accidental full superuser access
    user.save()

    token, _ = Token.objects.get_or_create(user=user)
    logger.info(f"New user registered: {username}, role={role}")

    return Response({
        'username': user.username,
        'role': role,
        'token': token.key
    }, status=status.HTTP_201_CREATED)
