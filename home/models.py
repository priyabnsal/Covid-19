from django.db import models

# Create your models here.
class Contact(models.Model):
    # id = models.AutoField(primary_key=True)
    name= models.CharField(max_length=122)
    email=models.CharField(max_length=122)
    message=models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name

class PredResults(models.Model):

    sepal_length = models.FloatField()
    sepal_width = models.FloatField()
    petal_length = models.FloatField()
    petal_width = models.FloatField()
    classification = models.CharField(max_length=30)

    def __str__(self):
        return self.classification

    