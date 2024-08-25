# monapp/models.py
from datetime import timezone
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
    
class CreditPurchaseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()  # Montant des crédits achetés
    price = models.IntegerField()  # Prix payé pour les crédits (en centimes, par exemple)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.amount} credits - {self.price} - {self.timestamp}'
    

class PromptHistory(models.Model):
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name='history')
    image = models.ImageField(upload_to='generated_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Utilisation de str() pour s'assurer que les valeurs sont converties en chaînes
        return f"History for {str(self.prompt.description)} at {str(self.created_at)}"