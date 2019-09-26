from django.shortcuts import render
from rest_framework.views import APIView, Response, status
from rest_framework.decorators import api_view
# Used to get current site info
from django.contrib.sites.shortcuts import get_current_site
import json
# Used for authentication
from requests import request, session, Request, Session
import requests
from requests.auth import HTTPBasicAuth
# User form
from .form import UserForm, UserCreationForm, LogoutForm
# for email generating template
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse
# for url parse
# for url join
import urllib.parse

# for encoding base64
from base64 import b64decode, b64encode, urlsafe_b64decode, urlsafe_b64encode
import base64


# Create your common services here.
class JwtToken:
    def __init__(self, username, group, email):
        self.token_service_host_port = ["http://localhost", "5004"]
        self.token_service_base_url = ':'.join(self.token_service_host_port)
        self.get_token_path = [self.token_service_base_url, 'jwt/get_token/']
        self.url = '/'.join(self.get_token_path)
        self.username = username
        self.group = group
        self.email = email

    def get_token(self):
        #response = requests.post(url='http://{}:{}/o/revoke_token/'.format(us_host, us_port), data=data)
        # Token service host name and port
        print("-- Token Service url (to get token): ", self.url)
        url = self.url
        formdata = {'username': self.username, 'group':self.group, 'email': self.email }
        response = requests.post(url, data=formdata)

        try:
            response.raise_for_status()
            # Must have been a 200 status code
            # json_obj = response.json()
            # json_obj = {'data': response.json(), 'status_code': response.status_code, 'url':url}
            # print("--Return response --", json_obj)
            json_obj = {'data': response.json(), 'status_code': response.status_code}
            # return json_obj
            return json_obj
        except requests.exceptions.HTTPError as e:
            json_obj = {'data': response.json(), 'status_code': response.status_code, 'url': url}
            return json_obj



        return Response({'log_msg': 'Get token success', 'url': self.url}, status=status.HTTP_200_OK)