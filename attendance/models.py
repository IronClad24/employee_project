"""
Model defining attendance records for employees. Enforces one record per employee per date.
"""
from django.db import models
from employees.models import Employee


class Attendance(models.Model):
    """Tracks attendance status of employees for specific dates."""
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='attendances',
        help_text="Employee associated with this attendance record"
    )
    date = models.DateField(
        help_text="Date of the attendance entry"
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        help_text="Attendance status: Present, Absent, or Late"
    )

    class Meta:
        unique_together = ('employee', 'date')
        verbose_name_plural = 'Attendance records'

    def __str__(self) -> str:
        return f"{self.employee.name} - {self.get_status_display()} on {self.date}"