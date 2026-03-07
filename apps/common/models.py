from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

class Page(models.Model):

    url = models.URLField()
    title = models.TextField()
    description = models.TextField()

    class Meta:
        db_table = "pages"
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")


from django.db import models


class FileProcessingTask(models.Model):

    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False
    )

    file = models.FileField(upload_to="uploads/")

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("processing", "Processing"),
            ("completed", "Completed"),
            ("failed", "Failed"),
            ("cancelled", "Cancelled"),
        ],
        default="pending",
    )

    progress = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)


class WebhookEvent(models.Model):
    event_id = models.CharField(max_length=255, unique=True)
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event_id