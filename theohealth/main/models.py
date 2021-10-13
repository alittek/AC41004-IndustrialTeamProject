from django.db import models
from django.contrib.auth.models import User

import json
import os
import pandas as pd
from datetime import datetime
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class Therapist(models.Model):
    """
    A Model that represents a Therapist, i.e. Physiotherapist, that can manage multiple Athletes.
    A Therapist is linked with a User object via the auth_user attribute. This makes it so that 
    """
    auth_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, default='')
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    def __str__(self):
        return self.first_name + " " + self.last_name

class Athlete(models.Model):
    """
    An Athlete represents an Athlete who has had an injury and is now using theohealth to support his recovery.
    This model is associated with a auth.User for authentication and a Therapist objects for linking Therapists and Athletes.
    """
    auth_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, default='')
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64, default='')
    last_name = models.CharField(max_length=64, default= '')
    contact_nb = models.CharField(max_length=64, default= '')
    email = models.CharField(max_length=64, default= '')
    phone_nb = models.CharField(max_length=64, default= '')
    injury = models.CharField(max_length=256, default= '')
    
    def __str__(self):
        return self.first_name + " " + self.last_name

class Workout(models.Model):
    """
    A model to store a Workout in the database. Provides helper functions, e.g. readings_from_file can be used to read sensor values directly from file and returns them as JSON string.
    """
    date = models.DateField()
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)

    # Displays the name of the Athlete in the workout
    def __str__(self):
        return str(self.date) + " " + self.athlete.__str__()

    # Stores fields in a 3D array
    def readings_from_file(self):
        readings = []
        for i in range(1, 5):
            # Must use path from the Python shell (manage.py), not from /main!
            df = pd.read_csv('main/SensorTest-set2/SensorTest-sensor' + str(i) + '.csv')
            values = []
            # Zips the columns together so the time and value can be accessed together
            [values.append(record) for record in zip(df.time, df.value)]
            # Appends as sensor(num)
            readings.append(values)

        # JSON to be able to read it into JS
        return json.dumps(readings)

class SensorReading(models.Model):
    """
    A model for individual reading. 
    Each reading is connected to a workout id.
    """
    workout_num = models.ForeignKey(Workout, on_delete=models.CASCADE)
    sensor_num = models.IntegerField()
    timestamp = models.DateTimeField()
    heatvalue = models.IntegerField()

    def __str__(self):
        return str(self.sensor_num) + " " + str(self.timestamp)
