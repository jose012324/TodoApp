from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Todo(models.Model):
    STATUS = (
        ('inprogress', 'InProgress'),
        ('done', 'Done')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos', null=True)
    description = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=STATUS, default='inprogress')

    def __str__(self):
        return self.description