"""Django admin configuration for tracker models."""

from django.contrib import admin
from .models import Status, Scheme, Case, CaseNote


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    """Admin list/edit settings for case statuses."""
    list_display = ('name', 'is_closed', 'order')
    list_editable = ('is_closed', 'order')


@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    """Admin list settings for pension schemes."""
    list_display = ('code', 'name')


class CaseNoteInline(admin.TabularInline):
    """Inline note editor embedded on case admin pages."""
    model = CaseNote
    extra = 0


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    """Admin configuration for tracking and searching workflow cases."""
    list_display = ('reference', 'title', 'status', 'priority', 'scheme', 'assigned_to', 'updated_at')
    list_filter = ('status', 'priority', 'scheme')
    search_fields = ('reference', 'title')
    inlines = [CaseNoteInline]


@admin.register(CaseNote)
class CaseNoteAdmin(admin.ModelAdmin):
    """Admin list settings for case notes."""
    list_display = ('case', 'created_by', 'created_at')
