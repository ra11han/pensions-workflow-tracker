"""Model forms used by tracker create/update and note workflows."""

from django import forms
from .models import Case, CaseNote


class CaseForm(forms.ModelForm):
    """Form for creating and editing tracker cases."""
    class Meta:
        model = Case
        fields = ['reference', 'title', 'description', 'status', 'priority', 'scheme', 'assigned_to', 'due_date']


class CaseNoteForm(forms.ModelForm):
    """Form for adding notes to an existing case."""
    class Meta:
        model = CaseNote
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3}),
        }
