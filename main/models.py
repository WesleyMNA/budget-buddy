from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class Category(models.Model):
    CATEGORY_CHOICES = {
        'F': 'Fixed',
        'G': 'Goal',
        'I': 'Investment',
        'K': 'Knowledge',
        'P': 'Pleasures',
    }

    category = models.CharField(
        max_length=1,
        choices=CATEGORY_CHOICES,
        primary_key=True
    )

    def __str__(self):
        return self.get_category_display()


class Budget(models.Model):
    percentage = models.IntegerField(
        default=20,
        null=False
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Expense(models.Model):
    title = models.CharField(
        max_length=100,
        null=False,
        unique=True,
    )
    value = models.FloatField(null=False)
    date = models.DateField(
        null=False,
        default=now
    )
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        default='F'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Revenue(models.Model):
    class Category(models.IntegerChoices):
        WAGE = 1
        ADVANCE = 2
        DIVIDEND = 3
        OTHER = 4

    title = models.CharField(
        max_length=100,
        null=False,
        unique=True,
    )
    value = models.FloatField(null=False)
    date = models.DateField(
        null=False,
        default=now
    )
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    category = models.IntegerField(
        null=False,
        choices=Category,
        default=Category.WAGE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
