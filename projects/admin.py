from django.contrib import admin
from django.utils.html import format_html
 
from .models import Project, ProjectImage, Technology
 
 
@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ["name", "icon_preview"]
    search_fields = ["name"]
 
    def icon_preview(self, obj):
        if obj.icon_url:
            return format_html(
                '<img src="{}" style="height:20px;width:20px;object-fit:contain;" />',
                obj.icon_url,
            )
        return "—"
    icon_preview.short_description = "Icon"
 
 
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ["image_preview", "image", "caption", "sort_order"]
    readonly_fields = ["image_preview"]
    ordering = ["sort_order"]
 
    def image_preview(self, obj):
        if obj.pk and obj.image:
            return format_html(
                '<img src="{}" style="height:60px;border-radius:4px;" />',
                obj.image.url,
            )
        return "No image yet"
    image_preview.short_description = "Preview"
 
 
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "status",
        "is_featured",
        "tech_list",
        "created_at",
    ]
    list_filter = ["status", "is_featured", "technologies"]
    search_fields = ["title", "short_desc", "description"]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["technologies"]
    readonly_fields = ["id", "created_at", "updated_at"]
    inlines = [ProjectImageInline]
 
    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "slug", "short_desc", "description")
        }),
        ("Links & Media", {
            "fields": ("live_link", "github_link", "video_url")
        }),
        ("Tech Stack", {
            "fields": ("technologies",)
        }),
        ("Publishing", {
            "fields": ("status", "is_featured")
        }),
        ("Metadata", {
            "fields": ("id", "created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )
 
    def tech_list(self, obj):
        return ", ".join(t.name for t in obj.technologies.all())
    tech_list.short_description = "Technologies"
