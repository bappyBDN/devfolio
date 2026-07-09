from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
 
 
class Experience(models.Model):
    """
    A single work-history entry for the resume timeline.
    """
    company_name = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField(
        blank=True,
        null=True,
        help_text="Leave blank if this is a current position.",
    )
    is_current = models.BooleanField(default=False)
    description = models.TextField(help_text="Key responsibilities / achievements.")
 
    class Meta:
        ordering = ["-is_current", "-start_date"]
 
    def __str__(self):
        return f"{self.role} @ {self.company_name}"
 
    def clean(self):
        """
        Cross-field validation:
        - If is_current is True, end_date is optional (and gets cleared).
        - If is_current is False, end_date is required.
        - end_date can never be earlier than start_date.
        """
        if self.is_current:
            self.end_date = None
        elif not self.end_date:
            raise ValidationError({
                "end_date": "End date is required unless this is marked as a current position."
            })
 
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError({
                "end_date": "End date cannot be earlier than the start date."
            })
 
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
 
 
class Education(models.Model):
    """
    A single education entry for the resume timeline.
    """
    institution_name = models.CharField(max_length=200)
    degree = models.CharField(max_length=150)
    passing_year = models.PositiveIntegerField()
    result = models.CharField(
        max_length=50,
        help_text="e.g. CGPA 3.85 / First Class / 90%",
    )
 
    class Meta:
        ordering = ["-passing_year"]
        verbose_name_plural = "Education"
 
    def __str__(self):
        return f"{self.degree} - {self.institution_name}"
 
 
class Skill(models.Model):
    """
    A single skill/tech entry with a proficiency level, grouped by category.
    """
    class Category(models.TextChoices):
        BACKEND = "backend", "Backend"
        FRONTEND = "frontend", "Frontend"
        AI_ML = "ai_ml", "AI/ML"
        DATABASE = "database", "Database"
        DEVOPS = "devops", "DevOps"
        OTHER = "other", "Other"
 
    name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER,
    )
    proficiency_percentage = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="1-100",
    )
 
    class Meta:
        ordering = ["category", "-proficiency_percentage"]
 
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"