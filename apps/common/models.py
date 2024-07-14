from django.db import models


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SubEmail(models.Model):
    email = models.EmailField(max_length=225, unique=True, null=True, blank=True)

    def __str__(self):
        return self.email
    