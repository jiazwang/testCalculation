from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context 
from django.views.generic.base import TemplateView 
from airapp.models import Airport
from django.core import serializers
import os, re, math
import json
from django import forms

#########################

def km2mile(x):
	'''a function to convert km to mile'''
	return int(x * 0.621371)

def calc_dist(lat1, lon1, lat2, lon2):
	'''a function to calculate the distance in miles between two 
	points on the earth, given their latitudes and longitudes in degrees'''

	# LAX
	#lat2 = math.radians(33.9425)
	#lon2 = math.radians(118.4072)
	# JFK
	#lat1 = math.radians(40.6397)
	#lon1 = math.radians(73.7789)

	# jfk -> lax is 2467 miles

	# covert degrees to radians
	lat1 = math.radians(lat1)
	lon1 = math.radians(lon1)
	lat2 = math.radians(lat2)
	lon2 = math.radians(lon2)

	# get the differences
	delta_lat = lat2 - lat1
	delta_lon = lon2 - lon1

 	# print(delta_lat)
 	# print(delta_lon)

	# Haversine formula, 
	# from http://www.movable-type.co.uk/scripts/latlong.html
	a = ((math.sin(delta_lat/2))**2) + math.cos(lat1)*math.cos(lat2)*((math.sin(delta_lon/2))**2) 
	c = 2 * math.atan2(a**0.5, (1-a)**0.5)
	# earth's radius in km
	earth_radius = 6371 
	# return distance in miles
	return km2mile(earth_radius * c)

class MyForm(forms.Form):
	'''A class for a form with two airport codes'''
	code1 = forms.CharField(max_length=50)
	code2 = forms.CharField(max_length=50)


def formview(request):
	# If the form has been submitted...
	if request.method == 'POST': 

		# A form bound to the POST data that has fields for user name and user password
		form = MyForm(request.POST) 

		# All validation rules pass
		if form.is_valid(): 

			# first airport code
			code1 = form.cleaned_data['code1']
			# second airport code
			code2 = form.cleaned_data['code2']

			# check that codes exists in database
			if ( Airport.objects.filter(code=code1).exists() and \
			Airport.objects.filter(code=code2).exists()):

				# calculate dist bet the airports from their latitudes and longitudes
				mylat1 = Airport.objects.get(code=code1).get_lat()
				mylon1 = Airport.objects.get(code=code1).get_lon()
				mylat2 = Airport.objects.get(code=code2).get_lat()
				mylon2 = Airport.objects.get(code=code2).get_lon()
				mydist = calc_dist(mylat1, mylon1, mylat2, mylon2)

				# render out.html, a page telling the user the distance
				return render(request, 'airapp/out.html', {'distance':mydist})

			# if not, go to "fail" page
			else:
				# Redirect to fail page after POST
				return HttpResponseRedirect('/airapp/fail/')

	else:
		# An unbound form
		form = MyForm()

	# pass variables: form
	return render(request, 'airapp/formtemplate.html', {'form': form})

def failview(request):
	'''A view to send user to the fail page if he enters the wrong airport codes'''

	return render(request, 'airapp/fail.html')

def getnamesview(request):
	'''This view is for autocompleting - see tutorial at 
	http://flaviusim.com/blog/AJAX-Autocomplete-Search-with-Django-and-jQuery/'''

	if request.is_ajax():
		q = request.GET.get('term', '')
		airports = Airport.objects.filter(longname__icontains = q )[:20]
		results = []
		for airport in airports:
			airport_json = {}
			airport_json['id'] = airport.code
			airport_json['label'] = airport.longname
			airport_json['value'] = airport.code
			results.append(airport_json)
		data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)