"""
Management command to seed the database with fake data.
Generates departments, employees, attendance for the last 30 days, and three performance reviews per employee.
"""
from django.core.management.base import BaseCommand
from faker import Faker
import random
from datetime import date, timedelta
from employees.models import Department, Employee, Performance
from attendance.models import Attendance


class Command(BaseCommand):
    help = 'Seed database with departments, employees, attendance, and performance records.'

    def handle(self, *args, **options):
        fake = Faker()
        # Create or fetch predefined departments
        department_names = ['HR', 'Engineering', 'Sales', 'Marketing', 'Finance']
        departments = [
            Department.objects.get_or_create(name=name)[0]
            for name in department_names
        ]

        # Create employees with assigned departments
        employees = []
        for _ in range(50):
            department = random.choice(departments)
            employee = Employee.objects.create(
                name=fake.name(),
                email=fake.unique.email(),
                phone_number=fake.phone_number(),
                address=fake.address(),
                date_of_joining=fake.date_between(start_date='-5y', end_date='today'),
                department=department
            )
            employees.append(employee)

        # Generate attendance entries for each employee over the past 30 days
        for employee in employees:
            for days_ago in range(30):
                entry_date = date.today() - timedelta(days=days_ago)
                status = random.choices(
                    population=['P', 'A', 'L'],
                    weights=[0.8, 0.1, 0.1],
                    k=1
                )[0]
                Attendance.objects.create(
                    employee=employee,
                    date=entry_date,
                    status=status
                )

        # Create three performance reviews per employee
        for employee in employees:
            for _ in range(3):
                review_date = fake.date_between(
                    start_date=employee.date_of_joining,
                    end_date='today'
                )
                rating = random.randint(1, 5)
                Performance.objects.create(
                    employee=employee,
                    rating=rating,
                    review_date=review_date
                )

        self.stdout.write(
            self.style.SUCCESS('Database seeding completed successfully.')
        )
