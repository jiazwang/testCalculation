from django.db import models
from django.forms import ModelForm

# read the django docs on models: 
# https://docs.djangoproject.com/en/dev/topics/db/models/


# a model for an airport
class Airport(models.Model):
    '''class representing an airport'''

    # airport letter code (usu 3 or 4 letters)
    code = models.CharField('Code', max_length=10)
    # long name (city plus airport name)
    longname = models.CharField('Name', max_length=100)
    # airport latitude in degrees
    latitude = models.DecimalField('Latitude', max_digits=8, decimal_places=5)
    # airport longitude in degrees
    longitude = models.DecimalField('Latitude', max_digits=8, decimal_places=5)

    # methods
    def get_id(self):
        return self.id

    def get_code(self):
        return self.code

    def get_name(self):
        return self.longname

    def get_lat(self):
        return self.latitude

    def get_lon(self):
        return self.longitude