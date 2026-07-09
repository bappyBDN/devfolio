
from django.contrib import admin
 
from .models import Message
 
 
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["sender_name", "subject", "is_read", "created_at"]
    list_filter = ["is_read", "created_at"]
    search_fields = ["sender_name", "sender_email"]
    ordering = ["-created_at"]
    actions = ["mark_as_read", "mark_as_unread"]
 
    # Everything the visitor submitted is read-only; staff can only
    # toggle is_read (either inline via the checkbox in list_display,
    # or on the detail page, or via the bulk actions below).
    readonly_fields = [
        "sender_name",
        "sender_email",
        "subject",
        "message",
        "created_at",
    ]
 
    fieldsets = (
        ("Submitted by visitor (read-only)", {
            "fields": ("sender_name", "sender_email", "subject", "message", "created_at")
        }),
        ("Staff action", {
            "fields": ("is_read",)
        }),
    )
 
    def has_add_permission(self, request):
        # Messages only ever come in through the public contact form,
        # never created by hand in the admin.
        return False
 
    def has_delete_permission(self, request, obj=None):
        # Keep a full audit trail of every message received.
        # Flip this to True later if you want cleanup capability.
        return True
 
    @admin.action(description="Mark selected messages as read")
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} message(s) marked as read.")
 
    @admin.action(description="Mark selected messages as unread")
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f"{updated} message(s) marked as unread.")