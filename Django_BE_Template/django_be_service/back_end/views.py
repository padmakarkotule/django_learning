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

# Create your views here.
# Used for post call
class Create_post(APIView):

    # def post(self, request, format=None): formats are api/json, text/html etc.
    def post(self, request, format=None):
        # Get url path of this class
        path = request.path
        # print("---path--", path)

        # User form
        form = UserForm(request.data)
        if form.is_valid():
            username = form.cleaned_data['username']
            groups = form.cleaned_data['group']
            email = form.cleaned_data['email']
            print("--In Create/post view, username, groups and email:", username, groups, email)

            #'token_type': token_type
            user_data =  payload = {
                'username': username,
                'groups': groups,
                'email': email,
            }
            if payload:
                log_msg = "Token sent"
                return Response({'data': user_data, 'log_msg': log_msg}, status=status.HTTP_200_OK, content_type='application/json')
            else:
                error_msg = "Token not generated, Please try again."
                return Response({'error_msg': error_msg}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": form.errors.as_json()}, status=400)


class List_get(APIView):

    def get(self, request, format=None):
        # Get url path of this class
        path = request.path
        # print("---path--", path)

        # User form
        form = UserForm(request.data)
        if form.is_valid():
            username = form.cleaned_data['username']
            groups = form.cleaned_data['group']
            email = form.cleaned_data['email']
            print("--In List/get username, groups and email:", username, groups, email)

            user_data =  payload = {
                'username': username,
                'groups': groups,
                'email': email,
            }
            if payload:
                log_msg = "List data success"
                return Response({'data': user_data, 'log_msg': log_msg}, status=status.HTTP_200_OK, content_type='application/json')
            else:
                error_msg = "Data not generated, Please try again."
                return Response({'error_msg': error_msg}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error_msg": form.errors.as_json()}, status=400)

