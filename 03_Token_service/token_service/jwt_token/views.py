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
from django.utils.timezone import now, timedelta
# for url join
import urllib.parse

# form
from .form import UserForm
# Jwt and oauth2
from base64 import b64decode, b64encode, urlsafe_b64decode, urlsafe_b64encode
import base64
import jwt


# Create your views here.
# Help tutorial link -https://medium.com/python-pandemonium/json-web-token-based-authentication-in-django-b6dcfa42a332

class GetToken(APIView):

    def post(self, request, format=None):
        path = request.path
        # print("---path--", path)
        form = UserForm(request.data)
        if form.is_valid():
            username = form.cleaned_data['username']
            group = form.cleaned_data['group']
            email = form.cleaned_data['email']
            print("-- In Token Service:", username, group, email)

            # Other data
            client_id = 'Django learning'
            client_secret = 'django'
            grant_type = 'password'
            scope = 'read write',
            expires_in = 300
            token_type = 'Bearer',

            # Generate jwt token

            payload = {
                'username': username,
                'group': group,
                'email': email,
                'client_id': client_id,
                'client_secret': client_secret,
                'grant_type': grant_type,
                'scope': scope,
                'expires_in': expires_in,
                'token_type': token_type,
            }
            jwt_token = jwt.encode(payload, 'SECRET', algorithm='HS256')
            if jwt_token:
                return Response({'jwt_token': jwt_token, 'log_msg': "Token sent."}, status=status.HTTP_200_OK)
            else:
                error_msg = "Token not generated, Please try again."
                return Response({'error_msg': error_msg}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"error": form.errors.as_json()}, status=400)


class VerifyToken(APIView):
    pass
