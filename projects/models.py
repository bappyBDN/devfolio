import uuid
 
from django.db import models
from django.utils.text import slugify
 
 
class Technology(models.Model):
    """
    Tech-stack / skill tags. Many-to-many with Project
    (one technology can belong to many projects, and vice versa).
    """
    name = models.CharField(max_length=50, unique=True)
    icon_url = models.URLField(
        blank=True,
        null=True,
        help_text="URL to a devicon/simple-icons SVG or similar."
    )
 
    class Meta:
        verbose_name = "Technology"
        verbose_name_plural = "Technologies"
        ordering = ["name"]
 
    def __str__(self):
        return self.name
 
 
class Project(models.Model):
    """
    Core portfolio project record.
    """
 
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
 
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
    short_desc = models.CharField(
        max_length=300,
        help_text="Short summary shown on project cards."
    )
    description = models.TextField(
        help_text="Full project write-up. Supports Markdown."
    )
    live_link = models.URLField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    video_url = models.URLField(
        blank=True,
        null=True,
        help_text="YouTube/Vimeo embed link (no direct video uploads)."
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    is_featured = models.BooleanField(default=False)
 
    technologies = models.ManyToManyField(
        Technology,
        related_name="projects",
        blank=True,
    )
 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        ordering = ["-is_featured", "-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["slug"]),
        ]
 
    def __str__(self):
        return self.title
 
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            # Ensure uniqueness even if two projects share a title.
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)
 
 
class ProjectImage(models.Model):
    """
    Screenshot gallery for a project. One-to-Many with Project.
    """
    project = models.ForeignKey(
        Project,
        related_name="images",
        on_delete=models.CASCADE,
    )
    # Local storage for now (Phase 1). Swap the field/storage backend
    # to Cloudinary in a later phase without touching the schema shape.
    image = models.ImageField(upload_to="projects/gallery/%Y/%m/")
    caption = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
 
    class Meta:
        ordering = ["sort_order", "id"]
 
    def __str__(self):
        return f"{self.project.title} - image #{self.sort_order}"