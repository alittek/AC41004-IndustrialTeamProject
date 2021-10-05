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

class Workout(models.Model):
    date = models.DateField()
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)

    # Displays the name of the Athlete in the workout
    def __str__(self):
        return str(self.date) + " " + self.athlete.__str__()

# Individual reading, each reading is connected to a workout id
class SensorReading(models.Model):
    workout_num = models.ForeignKey(Workout, on_delete=models.CASCADE)
    sensor_num = models.IntegerField()
    timestamp = models.DateTimeField()
    heatvalue = models.IntegerField()

    def __str__(self):
        return str(self.sensor_num) + " " + str(self.timestamp)