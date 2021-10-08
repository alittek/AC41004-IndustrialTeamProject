from django.db import models

import os
import pandas as pd
from datetime import datetime
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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

    # Stores fields in a 2D data structure
    def readings_from_file(self):
        # Dict used to store readings from all 4 files
        readings = {}
        for i in range(1, 5):
            # Must use path from the Python shell (manage.py), not from /main!
            df = pd.read_csv('main/SensorTest-set2/SensorTest-sensor' + str(i) + '.csv')
            # Appends as sensor(num)
            readings['sensor' + str(i)] = df

            # Latter part is a mask for the input from the CSV file
            # x and y are the axis of the graph
            x = df['time'].map(lambda x: datetime.strptime(str(x), '%Y-%m-%dT%H:%M:%S.%fZ'))
            y = df['value']

            # Plot
            plt.plot(x,y)
            # Simplify the x-labels
            plt.gcf().autofmt_xdate()

            #plt.savefig('debugging_graph' + str(i) + '.png')

            # Shows the graph (Doesn't work in terminal), for debugging remove comment for line above
            plt.show()
        return readings

# Individual reading, each reading is connected to a workout id
class SensorReading(models.Model):
    workout_num = models.ForeignKey(Workout, on_delete=models.CASCADE)
    sensor_num = models.IntegerField()
    timestamp = models.DateTimeField()
    heatvalue = models.IntegerField()

    def __str__(self):
        return str(self.sensor_num) + " " + str(self.timestamp)