from django.db import models
from django.contrib.auth.models import User
# models need to be migrated into the database!


class Todo(models.Model):
    title = models.CharField(max_length=50)
    memo = models.TextField(blank=True, max_length=3000)
    creation_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):  # show project name in admin page instead of 'Project (1)'
        return self.title
