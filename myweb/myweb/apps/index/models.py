from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Author(models.Model):
    fullname = models.CharField(max_length=100, unique=True)
    born_date = models.CharField(max_length=50, blank=True, null=True)
    born_location = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True)
    message_sent = models.BooleanField(default=False)
    
    class Meta:
        app_label = 'index'  # Указываем принадлежность модели к приложению index

    def __str__(self):
        return f'{self.fullname}'

class Tag(models.Model):
    tag = models.CharField(max_length=150)
    
    def __str__(self) -> str:
        return f'{self.tag}'

class Quote(models.Model):
    quote = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    
    def __str__(self):
        return f"{self.quote},{self.author},{self.tag}"
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'userprofile'):
            instance.userprofile.first_name = instance.first_name
            instance.userprofile.last_name = instance.last_name
            instance.userprofile.email = instance.email
            instance.userprofile.save()
        else:
            UserProfile.objects.create(user=instance, first_name=instance.first_name, last_name=instance.last_name, email=instance.email)
