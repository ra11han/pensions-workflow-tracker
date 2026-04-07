"""App configuration and post-migrate seeding for tracker data."""

import sys

from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class TrackerConfig(AppConfig):
    """Registers metadata for the tracker Django app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracker'


@receiver(post_migrate)
def seed_demo(sender, **kwargs):
    """Populate baseline lookup data and optional demo records after migrations."""
    # Only run for our app
    if sender.name != 'tracker':
        return

    # Keep test databases deterministic by avoiding post-migrate seed side effects.
    if 'test' in sys.argv:
        return

    from django.contrib.auth import get_user_model
    from .models import Status, Scheme, Case, CaseNote

    # Always ensure reference data exists
    if Status.objects.count() == 0:
        Status.objects.bulk_create([
            Status(name='New', is_closed=False, order=1),
            Status(name='In Progress', is_closed=False, order=2),
            Status(name='Awaiting Info', is_closed=False, order=3),
            Status(name='Completed', is_closed=True, order=4),
            Status(name='On Hold', is_closed=False, order=5),
        ])

    if Scheme.objects.count() == 0:
        Scheme.objects.bulk_create([
            Scheme(code='CSP', name='Core Scheme Process'),
            Scheme(code='DB', name='Defined Benefit'),
            Scheme(code='DC', name='Defined Contribution'),
        ])

    # Seed demo cases only when explicitly enabled, or when running locally in DEBUG
    if not (getattr(settings, 'SEED_DEMO_DATA', False) or settings.DEBUG):
        return

    if Case.objects.exists():
        return

    User = get_user_model()
    user = User.objects.order_by('id').first()
    if not user:
        return

    statuses = list(Status.objects.order_by('order'))
    schemes = list(Scheme.objects.all())

    demo_cases = []
    for i in range(1, 11):
        # Generate predictable sample cases for walkthroughs and screenshots.
        demo_cases.append(Case(
            reference=f"WF-{i:06d}",
            title=f"Demo workflow item {i}",
            description="Seeded demo case to help with initial walkthrough and screenshots.",
            status=statuses[min(i % len(statuses), len(statuses)-1)],
            priority=['Low', 'Medium', 'High'][i % 3],
            scheme=schemes[i % len(schemes)],
            created_by=user,
            assigned_to=user if i % 2 == 0 else None,
        ))

    Case.objects.bulk_create(demo_cases)

    for c in Case.objects.all()[:10]:
        CaseNote.objects.create(case=c, note='Initial note seeded for evidence screenshots.', created_by=user)
