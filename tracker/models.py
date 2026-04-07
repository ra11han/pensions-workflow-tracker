"""Database models for workflow cases, statuses, schemes, and notes."""

from django.conf import settings
from django.db import models


class Status(models.Model):
    """Represents a stage in the lifecycle of a workflow case."""
    name = models.CharField(max_length=50, unique=True)
    is_closed = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'statuses'

    def __str__(self):
        return self.name


class Scheme(models.Model):
    """Represents the pension scheme associated with a case."""
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


class Case(models.Model):
    """Primary work item tracked in the application."""
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    reference = models.CharField(max_length=30, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    scheme = models.ForeignKey(Scheme, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_cases')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_cases')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.reference


class CaseNote(models.Model):
    """Timestamped note attached to a case for audit/history context."""
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='notes')
    note = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Note for {self.case.reference}"
