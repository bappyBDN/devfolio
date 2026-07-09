import uuid
 
from django.db import models
from django.utils.text import slugify
 
 
class Blog(models.Model):
    """
    Technical blog post. Markdown content, rendered on the frontend
    in a later phase.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
        help_text="Auto-generated from the title if left blank.",
    )
    content = models.TextField(help_text="Full post body. Supports Markdown.")
    cover_image = models.ImageField(
        upload_to="blog/covers/%Y/%m/",
        blank=True,
        null=True,
    )
    views_count = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_published"]),
            models.Index(fields=["slug"]),
        ]
 
    def __str__(self):
        return self.title
 
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Blog.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)
