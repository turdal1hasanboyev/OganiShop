from django.db import models
from apps.common.models import BaseModel


class Contact(BaseModel):
    name = models.CharField(max_length=225, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)   
    message = models.TextField(null=True, blank=True) 

    def __str__(self):
        return self.name
    