from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    
    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]
    def __str__(self):
        if self.full_name:
            return self.full_name
        else:
            return self.email or self.username

    @property
    def full_name(self):
        """ Returns the user's full name. """
        return f"{self.last_name} {self.first_name} {self.middle_name}"