from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from employees.models import Department, Employee, Performance



class DepartmentAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='adminpass')
        self.token, _ = Token.objects.get_or_create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.department = Department.objects.create(name='Engineering')

    def test_list_departments(self):
        response = self.client.get('/api/departments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_department(self):
        response = self.client.post('/api/departments/', {'name': 'HR'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class EmployeeAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='adminpass')
        self.token, _ = Token.objects.get_or_create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.department = Department.objects.create(name='IT')

    def test_create_employee(self):
        payload = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone_number': '1234567890',
            'address': '123 Street',
            'date_of_joining': '2024-01-01',
            'department_id': self.department.id  # Assuming serializer expects department_id
        }
        response = self.client.post('/api/employees/', payload)
        print("DEBUG employee:", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_employees(self):
        Employee.objects.create(
            name='Jane Smith', email='jane@example.com', phone_number='1234567890',
            address='ABC Road', date_of_joining='2023-01-01', department=self.department
        )
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PerformanceAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='adminpass')
        self.token, _ = Token.objects.get_or_create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.department = Department.objects.create(name='QA')
        self.employee = Employee.objects.create(
            name='Eve', email='eve@example.com', phone_number='0000000000',
            address='XYZ Lane', date_of_joining='2022-06-15', department=self.department
        )

    def test_create_performance(self):
        response = self.client.post('/api/performances/', {
            'employee_id': self.employee.id,  # Assuming serializer uses employee_id
            'rating': 4,
            'review_date': '2024-12-01'
        })
        print("DEBUG performance:", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_performance(self):
        Performance.objects.create(employee=self.employee, rating=5, review_date='2023-05-01')
        response = self.client.get('/api/performances/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
