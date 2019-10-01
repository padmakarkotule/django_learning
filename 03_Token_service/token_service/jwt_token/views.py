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
from rest_framework_jwt.utils import jwt_decode_handler
from .jwt_services import Jwt


# Create your views here.
# Help tutorial link -https://medium.com/python-pandemonium/json-web-token-based-authentication-in-django-b6dcfa42a332

class GetToken(APIView):

    def post(self, request, format=None):
        path = request.path
        # print("---path--", path)
        form = UserForm(request.data)
        if form.is_valid():
            username = form.cleaned_data['username']
            groups = form.cleaned_data['group']
            email = form.cleaned_data['email']
            """
            # updated on 39-9
            token_type = 'Bearer'
            print("-- In Token Service:", username, groups, email)

            # Other data
            client_id = 'Client_self'
            client_secret = 'Client_secret_self'
            # grant_type = 'password'
            # scope = 'read write',
            # expires_in = 300
            # token_type = 'Bearer',
            # 30-9
            """
            # Generate jwt token
            """
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
            """
            """
            # 309
            #'token_type': token_type
            payload =  payload = {
                'username': username,
                'groups': groups,
                'email': email,
                'client_id': client_id
            }

            SECRET = "JWT test token"
            #jwt_token = jwt.encode(payload, SECRET, algorithm='HS256')

            jwt_token = jwt.encode(payload, 'secret', 'HS256').decode('utf-8')
            print("\n Org_JWT-TOKEN:", jwt_token)
            jwt_token = json.dumps(jwt_token)
            print("\n-- AfterJsonDumps_JWT-TOKEN:", jwt_token)
            # 30-9
            """

            #jwt_token1 = Jwt(username, groups, email)
            jwt_token1 = Jwt(username)
            jwt_token = jwt_token1.get_token(groups, email)
            print("--In view Received jwt in view", type(jwt_token), jwt_token)
            if jwt_token:
                print("\n--In view JWT in if statment", type(jwt_token), jwt_token)
                return Response({'jwt_token': jwt_token, 'log_msg': "Token sent."}, status=status.HTTP_200_OK)
            else:
                error_msg = "Token not generated, Please try again."
                return Response({'error_msg': error_msg}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": form.errors.as_json()}, status=400)


class VerifyToken(APIView):

    def post(self, request, format=None):
        path = request.path
        """
        # 01-10
        #SECRET = "JWT test token"
        user = request.data['username']
        #header_info = request.META.get
        received_token = request.META.get('HTTP_AUTHORIZATION')
        print("\n-- In Verify token -- Received data", user, type(received_token), received_token)
        received_token_json_loads = json.loads(received_token)
        print("\n-- Received token after json load", user, type(received_token_json_loads), received_token_json_loads)
        #received_token_j = json.loads(received_token)
        #payload = jwt.decode(received_token, SECRET, algorithm='HS256')
        #payload = jwt.decode(received_token, 'secret', algorithm='HS256')
        # payload = jwt_decode_handler(received_token)

        # decoded = base64.b64decode(received_token)
        payload = jwt.decode(received_token_json_loads, 'secret', algorithm='HS256')
        if payload:
            username = payload['username']
            groups = payload['groups']
            email = payload['email']
            client_id = payload['client_id']

            user_group = 'users'
            print("\n-- Data after decode TOKEN:", user, username, groups, email, client_id)
        # 01-10
        """
        # Data in request.data
        username = request.data['username']
        received_token = request.META.get('HTTP_AUTHORIZATION')

        jwt_token = Jwt(username)
        verify_token = jwt_token.verify_token(received_token)
        if verify_token:
            return Response(verify_token, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


        """
        # 01-10
            if user == username and user_group == groups:
                print("\n--username and group verified by JWT success.")
                return Response({'log_msg': "Token verified."}, status=status.HTTP_200_OK)
            else:
                print("\n--JWT token encoded and decoded data mismatch")
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error_msg': "Token mismatch"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # 01-100
        """

        """
        def token():
            try:
                token = request.data['token']
                payload = jwt.decode(token, SECRET)
                return Response(payload, status=status.HTTP_200_OK)
            except:
                return Response({'error_msg': "Invalid token"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        """
        """
        payload = token()
        if payload:
            username = payload['username']
            groups = payload['groups']
            email = payload['email']
            token_type = payload['token_type']
            client_id = payload['client_id']

            user_group = 'users'
            print("To verify token received data", user, username, groups, email, token_type, client_id)
            if user == username and user_group == groups:
                return Response({'log_msg': "Token verified."}, status=status.HTTP_200_OK)
        else:
            return Response({'error_msg': "Token mismatch"}, status=status.HTTP_401_UNAUTHORIZED)
        """


