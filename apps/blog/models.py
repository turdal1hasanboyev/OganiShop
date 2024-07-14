from django.db import models
from apps.common.models import BaseModel
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify
from django.urls import reverse


class Category(BaseModel):
    name = models.CharField(max_length=225)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=225)

    def save(self, *args, **kwargs):  
        if not self.slug:
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    

class Tag(BaseModel):
    name = models.CharField(max_length=225)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=225)

    def save(self, *args, **kwargs):  
        if not self.slug:
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Blog(BaseModel):
    name = models.CharField(max_length=225)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=225)
    description = RichTextField(null=True, blank=True)
    image = models.ImageField(upload_to='blogs/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    avtor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def save(self, *args, **kwargs):  
        if not self.slug:
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("blog-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name
    