"""
Models defining Employee domain entities: Department, Employee, and Performance.
Each model encapsulates distinct data and relationships.
"""
from django.db import models


class Department(models.Model):
    """Model representing an organizational department."""
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Name of the department"
    )

    def __str__(self) -> str:
        return self.name


class Employee(models.Model):
    """Model representing an employee with personal and departmental details."""
    name = models.CharField(
        max_length=255,
        help_text="Full name of the employee"
    )
    email = models.EmailField(
        unique=True,
        help_text="Corporate or personal email address"
    )
    phone_number = models.CharField(
        max_length=50,
        help_text="Contact phone number"
    )
    address = models.TextField(
        help_text="Residential or mailing address"
    )
    date_of_joining = models.DateField(
        help_text="Date when the employee joined the organization"
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='employees',
        help_text="Department to which the employee belongs"
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.department.name})"


class Performance(models.Model):
    """Model capturing performance review entries for employees."""
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='performances',
        help_text="Employee under review"
    )
    rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        help_text="Performance rating on a scale from 1 to 5"
    )
    review_date = models.DateField(
        help_text="Date when the performance review was conducted"
    )

    def __str__(self) -> str:
        return f"{self.employee.name}: {self.rating} on {self.review_date}"
