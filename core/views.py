from django.shortcuts import render

from blog.models import Blog
from projects.models import Project
from resume.models import Education, Experience, Skill


def home_view(request):
    """
    Renders the public home page: featured projects, published blog
    posts, and currently active experience(s).
    """
    context = {
        "featured_projects": Project.objects.filter(
            is_featured=True,
            status=Project.Status.PUBLISHED,
        ).prefetch_related("technologies", "images"),
        "published_blogs": Blog.objects.filter(
            is_published=True
        ).order_by("-created_at")[:3],
        "active_experiences": Experience.objects.filter(is_current=True),
    }
    return render(request, "pages/home.html", context)


def resume_view(request):
    """
    Renders the public resume page: experience timeline, education,
    and skills grouped by category.
    """
    context = {
        # Experience.Meta.ordering already sorts current-first, newest-first
        "experiences": Experience.objects.all(),
        "educations": Education.objects.all(),
        # Skill.Meta.ordering already sorts by category, so regroup
        # in the template works without extra sorting here.
        "skills": Skill.objects.all(),
    }
    return render(request, "pages/resume.html", context)