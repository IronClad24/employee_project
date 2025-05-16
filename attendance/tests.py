from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from employees.models import Department, Employee
from attendance.models import Attendance
from datetime import date


class AttendanceAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='adminpass')
        self.token, _ = Token.objects.get_or_create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.department = Department.objects.create(name='Support')
        self.employee = Employee.objects.create(
            name='Mike', email='mike@example.com', phone_number='9876543210',
            address='Main St', date_of_joining='2022-09-01', department=self.department
        )

    def test_create_attendance(self):
        response = self.client.post('/api/attendance/', {
            'employee_id': self.employee.id,  # Assuming serializer uses employee_id
            'date': '2025-01-01',
            'status': 'P'
        })
        print("DEBUG attendance:", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_attendance(self):
        Attendance.objects.create(employee=self.employee, date=date.today(), status='P')
        response = self.client.get('/api/attendance/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
