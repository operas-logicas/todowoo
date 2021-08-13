from django.conf import settings
from django.db import models

# Create your models here.
class Todo(models.Model):
  title = models.CharField(max_length=100)
  memo = models.TextField(blank=True)
  created = models.DateTimeField(auto_now_add=True)
  completed = models.DateTimeField(null=True, blank=True)
  important = models.BooleanField(default=False)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

  def __str__(self):
    return self.title + ' - ' + str(self.created.strftime('%Y-%m-%d %H:%M')) + ' (' + str(self.user) + ')'
