from django.db import models
from django.utils.safestring import mark_safe
from django.conf import  settings


class Product(models.Model):
    CATEGORY_OPTIONS = (
        ('SEWING MACHINES','SEWING MACHINES'),
        ('COVERLOCK','COVERLOCK'),
        ('OVERLOCK','OVERLOCK'),
        ('ACCESSORIES','ACCESSORIES')
    )
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    count_in_stock = models.SmallIntegerField(default=1)
    in_stock = models.BooleanField(default=True)
    brand = models.CharField(max_length=150)
    has_sizes = models.BooleanField(default=False, blank=True)
    category = models.CharField(max_length=15, choices=CATEGORY_OPTIONS, default='OVERLOCK')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='products/')
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    num_reviews = models.SmallIntegerField(default=0, null=True, blank=True)

    def image_tag(self):
        if self.image:
            return mark_safe(
                    '<img src="%s" height="50" width="50">' % self.image.url)
        return "No image found"
    
    def __str__(self):
        return self.name
    

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,
                                null=True
                                )
    user = models.ForeignKey(
                             settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL,
                             null=True
                             )
    rating = models.SmallIntegerField(default=0, null=True, blank=True)
    review = models.TextField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s review on {self.product.name}"
