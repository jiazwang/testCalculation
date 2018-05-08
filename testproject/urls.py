from django.conf.urls import url
from airapp import views

# The main page is airapp/test. This is the gateway. 
# If the user successfully enters two airport codes, okay
# Otherwise, he goes to airapp/fail
# the airapp/get_names is used for autocomplete

urlpatterns = [
    url(r'^test/$', views.formview),
    # this is used for autocomplete
    url(r'^get_names/$', views.getnamesview),
    # this view is activated when the user input-ed codes are not found
    url(r'^fail/$', views.failview),
            ]
