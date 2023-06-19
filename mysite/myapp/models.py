from django.db import models


# Create your models here.
LABEL_TYPE = (
    ("positive", "positive"),
    ("negative", "negative"),
    ("neutral", "neutral")
)


class Sentiment(models.Model):
    text = models.TextField()
    label = models.CharField(choices=LABEL_TYPE, max_length=8)

    # def __str__(self):
    #     return self.text
