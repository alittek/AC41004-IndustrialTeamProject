from django.db import models

class Therapist(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    def __str__(self):
        return self.first_name + " " + self.last_name

class Athlete(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    birthdate = models.DateField()

    def __str__(self):
        return self.first_name + " " + self.last_name
