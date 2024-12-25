from django.db import models
from apps.account.models import Account


class Cv(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    job_title = models.CharField(max_length=50, null=True)
    prompt = models.TextField()
    cv_text = models.TextField(null=True)
    cv = models.FileField(upload_to='cv_pdfs/', null=True, blank=True)

    def __str__(self):
        return self.user.username