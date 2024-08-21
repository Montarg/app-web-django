# monapp/models.py
from django.db import models
from django.contrib.auth.models import  User



class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title


class Prompt(models.Model):
    # Identifiant unique du prompt
    id = models.AutoField(primary_key=True)

    # Clé étrangère vers le modèle User
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prompts')

    # Description textuelle du prompt
    description = models.TextField()

    # Date et heure de création du prompt
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prompt {self.id} by {self.user.username}"

class Style(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class CustomerUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credits = models.IntegerField(default=0)

    def __str__(self):
        return f"CustomerUser for {self.user.username}"