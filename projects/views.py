import markdown as md
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from .models import Project, Technology
from .utils import embed_url


def project_list_view(request):
    """
    Displays all published projects with optional technology filtering.
    """
    projects = Project.objects.filter(
        status=Project.Status.PUBLISHED
    ).prefetch_related("technologies", "images").order_by("-created_at")

    technologies = Technology.objects.all().order_by("name")

    selected_tech = request.GET.get("tech")
    if selected_tech:
        # Filter projects that have a technology matching the queried name (case-insensitive)
        projects = projects.filter(technologies__name__iexact=selected_tech)

    # Implement pagination (e.g., 9 projects per page)
    paginator = Paginator(projects, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "projects": page_obj.object_list,
        "technologies": technologies,
        "selected_tech": selected_tech,
    }
    return render(request, "pages/projects.html", context)


def project_detail_view(request, slug):
    """
    Displays a single project and renders its markdown description.
    """
    project = get_object_or_404(
        Project.objects.prefetch_related("technologies", "images"),
        slug=slug,
        status=Project.Status.PUBLISHED
    )

    # Render Markdown description to safe HTML
    rendered_description = mark_safe(
        md.markdown(
            project.description,
            extensions=["extra", "codehilite", "sane_lists"],
        )
    )

    # Fetch up to 3 related projects, excluding the current one
    related_projects = Project.objects.filter(
        status=Project.Status.PUBLISHED
    ).exclude(pk=project.pk).order_by("-created_at")[:3]

    context = {
        "project": project,
        "rendered_description": rendered_description,
        "related_projects": related_projects,
        # Pre-converted so the template just prints a plain URL.
        "video_embed_url": embed_url(project.video_url),
    }
    return render(request, "pages/project_detail.html", context)