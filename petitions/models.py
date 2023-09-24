from django.contrib.auth import get_user_model
from django.db import models

from tinymce.models import HTMLField


User = get_user_model()


class Petition(models.Model):
    title = models.CharField(max_length=255)
    description = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='petitions')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Петиция'
        verbose_name_plural = 'Петиции'


class PetitionImage(models.Model):
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='petitions/')

    def __str__(self):
        return self.petition.title

    class Meta:
        verbose_name = 'Изображение петиции'
        verbose_name_plural = 'Изображения петиций'


class PetitionComment(models.Model):
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий петиции'
        verbose_name_plural = 'Комментарии петиций'


class PetitionVote(models.Model):
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE, related_name='votes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    created_at = models.DateTimeField(auto_now_add=True)
    is_agree = models.BooleanField(default=True)

    def __str__(self):
        return self.petition.title

    class Meta:
        verbose_name = 'Голос петиции'
        verbose_name_plural = 'Голоса петиций'


class PetitionTag(models.Model):
    petitions = models.ManyToManyField(Petition, related_name='tags', blank=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег петиции'
        verbose_name_plural = 'Теги петиций'
