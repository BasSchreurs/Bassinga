from django.db import models

class FretTab(models.Model):
    name = models.CharField(max_length=100)
    E = models.TextField()
    A = models.TextField()
    D = models.TextField()
    G = models.TextField()
    position = models.PositiveIntegerField(default=0)  # manual sorting

    class Meta:
        ordering = ['position']  # ensures admin and queries respect the position

    def __str__(self):
        return self.name