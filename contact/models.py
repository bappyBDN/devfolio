from django.db import models
 
 
class Message(models.Model):
    """
    A message submitted through the public contact form.
    Read-only from the admin's perspective once submitted —
    the only thing staff should change is `is_read`.
    """
    sender_name = models.CharField(max_length=150)
    sender_email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_read"]),
        ]
 
    def __str__(self):
        return f"{self.sender_name} - {self.subject or '(no subject)'}"