"""Smoke tests that validate core tracker routing and permissions."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Status, Scheme, Case


class TrackerSmokeTests(TestCase):
    """Covers basic authentication and staff-only access rules."""
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='tester', password='pass12345')
        self.staff = User.objects.create_user(username='staff', password='pass12345', is_staff=True)

        self.status, _ = Status.objects.get_or_create(
            name='New',
            defaults={'is_closed': False, 'order': 1},
        )
        self.scheme, _ = Scheme.objects.get_or_create(
            code='CSP',
            defaults={'name': 'Core Scheme Process'},
        )
        self.case, _ = Case.objects.get_or_create(
            reference='WF-999999',
            defaults={
                'title': 'Test case',
                'description': 'desc',
                'status': self.status,
                'priority': 'Medium',
                'scheme': self.scheme,
                'created_by': self.user,
            },
        )

    def test_login_required_case_list(self):
        resp = self.client.get(reverse('case_list'))
        self.assertNotEqual(resp.status_code, 200)

    def test_case_list_ok_when_logged_in(self):
        self.client.login(username='tester', password='pass12345')
        resp = self.client.get(reverse('case_list'))
        self.assertEqual(resp.status_code, 200)

    def test_delete_requires_staff(self):
        self.client.login(username='tester', password='pass12345')
        resp = self.client.get(reverse('case_delete', args=[self.case.pk]))
        self.assertNotEqual(resp.status_code, 200)

        self.client.login(username='staff', password='pass12345')
        resp = self.client.get(reverse('case_delete', args=[self.case.pk]))
        self.assertEqual(resp.status_code, 200)

