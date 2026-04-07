"""View handlers for dashboard analytics and case management workflows."""

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CaseForm, CaseNoteForm
from .models import Case, Status, Scheme


def landing(request):
    """Render the unauthenticated landing page."""
    return render(request, 'tracker/landing.html')


@login_required
def dashboard(request):
    """Render summary metrics and lightweight workload insights."""
    due_soon_limit = 10
    open_cases = Case.objects.filter(status__is_closed=False, due_date__isnull=False).count()
    high_priority = Case.objects.filter(priority='High', status__is_closed=False).count()
    due_soon = Case.objects.filter(due_date__isnull=False, status__is_closed=False).order_by('due_date')[:due_soon_limit]
    by_status = (Case.objects.values('status__name')
                .annotate(total=Count('id'))
                .order_by('status__name'))

    return render(request, 'tracker/dashboard.html', {
        'open_cases': open_cases,
        'high_priority': high_priority,
        'due_soon': due_soon,
        'due_soon_limit': due_soon_limit,
        'by_status': by_status,
    })


@login_required
def case_list(request):
    """List cases with optional query-string filtering by key attributes."""
    qs = Case.objects.select_related('status', 'scheme', 'assigned_to')

    q = request.GET.get('q', '').strip()
    status_id = request.GET.get('status', '').strip()
    priority = request.GET.get('priority', '').strip()
    scheme_id = request.GET.get('scheme', '').strip()
    assigned = request.GET.get('assigned', '').strip()  # all / me / unassigned

    if q:
        # Match either title text or case reference from a single search box.
        qs = qs.filter(Q(title__icontains=q) | Q(reference__icontains=q))

    if status_id:
        qs = qs.filter(status_id=status_id)

    if priority:
        qs = qs.filter(priority=priority)

    if scheme_id:
        qs = qs.filter(scheme_id=scheme_id)

    if assigned == 'me':
        qs = qs.filter(assigned_to=request.user)
    elif assigned == 'unassigned':
        qs = qs.filter(assigned_to__isnull=True)

    statuses = Status.objects.all()
    schemes = Scheme.objects.all()
    priorities = [choice[0] for choice in Case.PRIORITY_CHOICES]

    return render(request, 'tracker/case_list.html', {
        'cases': qs.order_by('-updated_at'),
        'statuses': statuses,
        'schemes': schemes,
        'priorities': priorities,
        'filters': {
            'q': q,
            'status': status_id,
            'priority': priority,
            'scheme': scheme_id,
            'assigned': assigned,
        }
    })


@login_required
def case_detail(request, pk):
    """Display a case and accept note submissions for that case."""
    case = get_object_or_404(Case.objects.select_related('status', 'scheme', 'assigned_to', 'created_by'), pk=pk)

    if request.method == 'POST':
        note_form = CaseNoteForm(request.POST)
        if note_form.is_valid():
            note = note_form.save(commit=False)
            note.case = case
            note.created_by = request.user
            note.save()
            return redirect('case_detail', pk=pk)
    else:
        note_form = CaseNoteForm()

    return render(request, 'tracker/case_detail.html', {
        'case': case,
        'note_form': note_form,
    })


@login_required
def case_create(request):
    """Create a new case and attach the current user as creator."""
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            return redirect('case_detail', pk=obj.pk)
    else:
        form = CaseForm()

    return render(request, 'tracker/case_form.html', {'form': form, 'mode': 'Create'})


@login_required
def case_update(request, pk):
    """Edit an existing case record."""
    case = get_object_or_404(Case, pk=pk)
    if request.method == 'POST':
        form = CaseForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
            return redirect('case_detail', pk=pk)
    else:
        form = CaseForm(instance=case)

    return render(request, 'tracker/case_form.html', {'form': form, 'mode': 'Edit'})


@user_passes_test(lambda u: u.is_staff)
def case_delete(request, pk):
    """Delete a case, restricted to adnin or super users."""
    case = get_object_or_404(Case, pk=pk)
    if request.method == 'POST':
        case.delete()
        return redirect('case_list')
    return render(request, 'tracker/case_confirm_delete.html', {'case': case})
