from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class BlogCategory(models.Model):
    blogcategoryid = models.AutoField(primary_key=True)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category

class Blog(models.Model):
    CHOICES = (
        ('Approve', 'Approve'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected'),

    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='blog/', null=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=100, choices=CHOICES, null=True, blank=True, default="Pending")

    isdelete = models.BooleanField(default=False)