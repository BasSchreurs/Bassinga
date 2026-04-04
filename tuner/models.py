from django.db import models

class FretTab(models.Model):
    name = models.CharField(max_length=100)
    G = models.TextField()
    D = models.TextField()
    A = models.TextField()
    E = models.TextField()
    position = models.PositiveIntegerField(default=0)  # manual sorting

    class Meta:
        ordering = ['position']  # ensures admin and queries respect the position

    def __str__(self):
        return self.name