from django.test import TestCase
#from rest_framework.views import APIView, Response, status
import os
from django.conf import settings
from django.urls import reverse


# Create your tests here.
def get_token():
    #from django.conf import settings
    settings.configure(INSTALLED_APPS=['user_mgmt'], MIDDLEWARE_CLASSES=())
    #response = requests.post(url='http://{}:{}/o/revoke_token/'.format(us_host, us_port), data=data)


    # Token service host name and port
    token_service_host_port = ["http://localhost", "5004"]
    token_service_base_url = ':'.join(token_service_host_port)
    get_token_path = [token_service_base_url, 'jwt/get_token/']
    url = '/'.join(get_token_path)
    print("-- Token Service url (to get token): ", url)
    return "200_OK"

get_token()