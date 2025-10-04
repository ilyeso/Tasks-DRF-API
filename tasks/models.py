from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator

class Task(models.Model):
    TYPE_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ]
    
    label = models.CharField(max_length=50)
    description = models.TextField(max_length=300,blank=True)
    affected_to = models.ManyToManyField(User, related_name='tasks', blank=True)
    type = models.CharField(max_length=8, choices=TYPE_CHOICES, default='private')

    priority = models.PositiveSmallIntegerField( validators=[MinValueValidator(1),MaxValueValidator(5)],default=3)
    attached_file = models.FileField(
        upload_to='task_files/', null=True, blank=True,
        validators= [FileExtensionValidator(allowed_extensions=['pdf'])])
    
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return f"Task: {self.label}, Prio : {self.priority}"