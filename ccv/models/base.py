import uuid
from django.db import models
from ..constants.db_constants import DEFAULT_COLUMN_LENGTH


class Base(models.Model):
    """Abstract class """
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Organization(Base):
    name = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    subdivision = models.CharField(max_length=50, null=True, blank=True)


class OtherOrganization(Base):
    type = models.CharField(max_length=20, null=True, blank=True,
                            help_text="The type of organization, only if Other Organization is entered")
    name = models.CharField(max_length=DEFAULT_COLUMN_LENGTH, null=True, blank=True,
                            help_text="The organization's name, only if not in Organization list")


class CanadianCommonCv(Base):
    """Master table which links all entities like Identification, Education, Employment, Contribution, etc."""

    _id = models.UUIDField(max_length=40, db_index=True, editable=False, default=uuid.uuid4)
    slug = models.SlugField(help_text="Short label to be used in URL")

    class Meta:
        ordering = ["-id"]
