from django.db import models


class Contact(models.Model):
    email = models.EmailField(max_length=255, null=False, blank=False)
    subject = models.CharField(max_length=255, null=False, blank=False)
    message = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.email