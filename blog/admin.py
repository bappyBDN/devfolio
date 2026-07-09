from django.contrib import admin
from django.utils.html import format_html
 
from .models import Blog
 
 
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "cover_thumb",
        "is_published",
        "views_count",
        "created_at",
        "updated_at",
    ]
    list_filter = ["is_published", "created_at"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ["id", "views_count", "created_at", "updated_at"]
    ordering = ["-created_at"]
 
    fieldsets = (
        ("Post", {
            "fields": ("title", "slug", "cover_image", "content")
        }),
        ("Publishing", {
            "fields": ("is_published",)
        }),
        ("Metadata", {
            "fields": ("id", "views_count", "created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )
 
    def cover_thumb(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="height:40px;border-radius:4px;" />',
                obj.cover_image.url,
            )
        return "—"
    cover_thumb.short_description = "Cover"