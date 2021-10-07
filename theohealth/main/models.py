from django.db import models

class Therapist(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    def __str__(self):
        return self.first_name + " " + self.last_name

class Athlete(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64, default='')
    last_name = models.CharField(max_length=64, default= '')
    contact_nb = models.CharField(max_length=64, default= '')
    email = models.CharField(max_length=64, default= '')
    phone_nb = models.CharField(max_length=64, default= '')
    injury = models.CharField(max_length=64, default= '')
    
    def __str__(self):
        return self.first_name + " " + self.last_name
