
import markdown as md
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from .models import Blog

def blog_list_view(request):
    """
    Displays a paginated list of published blog posts.
    """
    posts_list = Blog.objects.filter(is_published=True).order_by('-created_at')
    
    paginator = Paginator(posts_list, 6) # 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'posts': page_obj.object_list,
    }
    return render(request, 'pages/blogs.html', context)

def blog_detail_view(request, slug):
    """
    Displays a single blog post and renders its content from Markdown.
    """
    post = get_object_or_404(Blog, slug=slug, is_published=True)
    
    # Increment view count (optional but good for analytics)
    post.views_count += 1
    post.save(update_fields=['views_count'])

    rendered_content = mark_safe(
        md.markdown(
            post.content,
            extensions=["extra", "codehilite", "sane_lists"],
        )
    )

    context = {
        'post': post,
        'rendered_content': rendered_content,
    }
    return render(request, 'pages/blog_detail.html', context)