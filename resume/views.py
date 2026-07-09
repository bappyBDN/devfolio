from django.shortcuts import render

from resume.models import Education, Experience, Skill

# ... keep your existing home_view here as-is ...


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