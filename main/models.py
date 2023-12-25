from django.db import models


class Budget(models.Model):
    CATEGORY_CHOICES = {
        'F': 'Fixed',
        'G': 'Goal',
        'I': 'Investment',
        'K': 'Knowledge',
        'P': 'Pleasures',
    }

    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        primary_key=True
    )
    percentage = models.IntegerField(default=20, null=False)


# class Expenses(models.Model):
#     pass
#
#
# class Revenue(models.Model):
#     pass
