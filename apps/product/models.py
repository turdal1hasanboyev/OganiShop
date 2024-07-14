from django.db import models
from apps.common.models import BaseModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify
from django.urls import reverse


class Category(BaseModel):
    name = models.CharField(max_length=225)
    image = models.ImageField(upload_to="cats/", null=True, blank=True)
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


class Banner(BaseModel):
    name = models.CharField(max_length=225)
    image = models.ImageField(upload_to='banners/')
    description = RichTextField(null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        blank=True, null=True,
    )
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE,
        null=True, blank=True,
        limit_choices_to={"parent__isnull": True},
        related_name="children")

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=225)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=225)
    banner = models.ForeignKey(Banner, on_delete=models.SET_NULL, null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    views = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    percentage = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        blank=True, null=True,
        related_name="products"        
    )
    tags = models.ManyToManyField(Tag, blank=True)

    def save(self, *args, **kwargs):  
        if not self.slug:
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("detail", kwargs={"slug": self.slug})

    @property
    def discount(self):
        if self.percentage:
            return self.price - (self.price * self.percentage) / 100
        return self.price
    
    @property
    def tag_list(self):
        return ', '.join([tag.name for tag in self.tags.all()])
    
    @property
    def avg_rate(self):
        rates = self.rates.annotate(avg_rate=models.Avg('rate'))
        return rates['avg_rate']
    
    @property
    def reviews_count(self):
        return self.rates.count()


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products')
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name


class Rate(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='rates')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    message = models.CharField(max_length=225, null=True, blank=True)
    rate = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.user.get_full_name} - {self.rate} - {self.product.name}"
