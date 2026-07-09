from django.contrib import admin
from django.utils.html import format_html
 
from .models import Education, Experience, Skill
 
 
@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = [
        "role",
        "company_name",
        "start_date",
        "end_date",
        "is_current",
    ]
    list_filter = ["is_current", "company_name"]
    search_fields = ["company_name", "role", "description"]
    ordering = ["-is_current", "-start_date"]
    fields = [
        "company_name",
        "role",
        "start_date",
        "is_current",
        "end_date",
        "description",
    ]
 
 
@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ["degree", "institution_name", "passing_year", "result"]
    list_filter = ["passing_year"]
    search_fields = ["institution_name", "degree"]
    ordering = ["-passing_year"]
 
 
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "proficiency_bar"]
    list_filter = ["category"]
    search_fields = ["name"]
    ordering = ["category", "-proficiency_percentage"]
 
    def proficiency_bar(self, obj):
        return format_html(
            '<div style="background:#eee;border-radius:4px;width:120px;">'
            '<div style="background:#4f46e5;color:white;text-align:right;'
            'padding:2px 4px;border-radius:4px;width:{}%;font-size:11px;">'
            "{}%</div></div>",
            obj.proficiency_percentage,
            obj.proficiency_percentage,
        )
    proficiency_bar.short_description = "Proficiency"