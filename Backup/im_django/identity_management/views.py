from django.shortcuts import render
from rest_framework.views import APIView, Response, status
from rest_framework.decorators import api_view
# Create user
from django.contrib.auth.models import User, UserManager
from django.contrib.auth import authenticate
# Used to get current site info
from django.contrib.sites.shortcuts import get_current_site
# Used for account activation to send mail (obj. convert in string)
#from django.template.loader import render_to_string
#from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse

## to get users
from .serializers import UserSerializer, UserSerializerGet, UserSerializerPost

from .form import UserForm, UserCreationForm, LogoutForm
import json
from requests import request, session

# Create your views here.


class Signup(APIView):

    """
    global user_create

    def user_create(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        print("\n--Received data to creat user - username, password, email --", self.username, self.password,
              self.email)
        try:
            user_create = User.objects.create_user(username=username, email=email, password=password)
            user_create.is_active = False
            user_create.save()
            username = user_create.username
            return Response({'username': username})
        except:
            return Response({'error': "User not created, internal system error"})
    """
    def post(self, request, format=None):
        form = UserCreationForm(request.data)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            #all_users = User.objects.all()
            #print("--all users in system", all_users)
            try:
                check_user = User.objects.get(username=username)
                if check_user:
                    print("---User already available in system --")
                    error_msg = 'username already available in system, pl. try with different username'
                    payload = {'error_msg': error_msg , 'username': username}
                    return Response(payload, status=status.HTTP_409_CONFLICT)
            except:
                #user_create = User.objects.create_user(username=username, email=email, password=password)
                user_create = User.objects.create_user(username=username, password=password, email=email)
                user_create.is_active = False
                user_create.save()
                # Data for sending mail to activate user
                pk = user_create.pk
                username = user_create.username
                email = user_create.email
                payload = {'log_msg': "User Created Successfully.", 'id':pk, 'username': username, 'email':email }
                return Response(payload, status=status.HTTP_201_CREATED)
                #else:
                #print("\n--username, password, email --", username, password, email)
                #print("\n--Received data to creat user - username, password, email --", username, password, email)
                #print("---Start creating user --")
                #create_user = user_create(self, username, password, email)
                #print("----User created and it's status is -", create_user.data, create_user.status_code)
                #if create_user:
                    #print("--User created --")
                    #print("Status of user create is -", create_user)
                    #print("--Create_user success, returning status")
                #   return Response(status=status.HTTP_201_CREATED)
                #else:
                #    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
                return Response({"error": form.errors.as_json()}, status=400)


@api_view(['GET'])
#def activate(request, uidb64, token):
def activate(request, id):
    try:
        id = id
        #token = token
        user = User.objects.get(pk=id)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None:
        user.is_active = True
        user.save()
        print(print("----- Activated -----"))
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        #return HttpResponse({'message','Account activated.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error':'Invalid link'}, status = status.HTTP_404_NOT_FOUND)


class auth_login(APIView):

    #def check_object_permissions(self, request, obj):
    path = request.__get__('path')
    print("----", path)

    def post(self, request, format=None):
        form = UserForm(request.data)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # print("---", username, password)
            user = authenticate(request, username=username, password=password)
            #print("data type", type(user))
            if user is not None and user.is_active:
                #uid = username
                #payload = {'log_message': "Authentication Successful.", 'username': username, 'uid': uid}
                payload = {'log_msg': "Authentication Successful.", 'username': username}
                #request.session['uid'] = payload['uid']
                #request.session['username'] = payload['username']
                #return Response({'log_message':"Authentication Successful.", 'user':user}, status=status.HTTP_200_OK)
                return Response(payload, status=status.HTTP_200_OK)
            else:
                error_msg = "Your username and password didn't match or check account activation mail. Please try again."
                payload = {"error_msg": error_msg , 'username': username}
                return Response(payload, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"log_msg": form.errors.as_json()}, status=status.HTTP_400_BAD_REQUEST)

class get_user_info(APIView):

    """
    def get(self, request):
        query = Users.objects.all()
        serializer = UserSerializerGet(query, many=True)
        return Response(serializer.data)
    """
    global check_auth
    def check_auth(self):

        # Returned Username after authentication - authenticate and get user info from IM service.
        IsAuthenticated = True
        username = 'user9'
        return Response({'IsAuthenticated':IsAuthenticated, 'username':username})

    def post(self, request, format=None):
        role = request.data['role']
        username = request.data['username']
        end_point_url = request.path
        current_site = get_current_site(request)
        method = request.method
        headers = request.headers

        """
        Under Rest, request is made up of :
            The endpoint
            The method
            The headers
            The data (or body)
        """

        try:
            username_in_session = request.session['username']
            user_request_user = request.user
        except:
            #username_in_session = 'Anonymoususer'
            username_in_session = None
            user_request_user = 'Anonymoususer'

        check_authentication = check_auth(self)
        IsAuthenticated = check_authentication.data['IsAuthenticated']
        payload = {'username':username, 'role':role, 'endpoint_url':end_point_url, 'user_in_session':username_in_session,
                   'user_request_user':user_request_user, 'current_site':current_site.name, 'method':method, 'head':headers}


        print("----Getting user info", payload)
        print("----IsAuthenticated user info", check_authentication.data['IsAuthenticated'])

        def check_permissions(self, request, user_data):
            self.user_data = user_data



        return Response(payload, status=status.HTTP_200_OK)


class ListUsers(APIView):
    def get(self, request):
        query = User.objects.all()
        #print(query)
        serializer = UserSerializerGet(query, many=True)
        data = serializer.data
        #print("---data--", data)
        return Response({'data':data})

    def post(self, request):
        # create accounts if post
        username = 'user4'
        password = 'Pass4321'
        email = 'user4@test.com'
        #uname = request.data['username']
        #try:
        #    reuser = User.objects.get(username=uname)
        #    print(reuser)
        #except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        #    print("not getting uname")

        create_user = User.objects.create_user(username=username, password=password, email=email)
        create_user.save()
        #pk= create_user.pk
        #print("\n----pk--",pk)

        return Response({'data':'testdata'})
