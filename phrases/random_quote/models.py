from django.db import models

# Create your models here
class Source(models.Model):
    SOURCE_TYPES = [
        ('movie', 'Фильм'),
        ('book', 'Книга'),
    ]
    name = models.CharField(unique=True, max_length=140)
    from_where = models.CharField(
        max_length=140,
        choices=SOURCE_TYPES,
        default='book',
        blank=False,
        null=False
    )

class Quote(models.Model):
    text = models.CharField(unique=True, max_length=140)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    weight = models.PositiveIntegerField(default=1)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)