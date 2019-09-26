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

# Common services
from .services import JwtToken
# Create your views here.


#@api_view(['GET'])
#def get_config(request, service_name):
def get_config(service_name):
    service_name = service_name
    #print("--service_name", service_name)
    if service_name == 'im_service':
        # Identity management server details
        host = "http://localhost:5002/"
        service_account = 'dladmin'
        sa_pass = 'Pass4321'
        url_login = host + 'auth_login/'
        im_service_details = {'url_login': url_login, 'sa_account': service_account, 'sa_account_pass':sa_pass}
        #return Response({'im_service_details': im_service_details}, status=status.HTTP_200_OK)
        return {'data':im_service_details, 'status': '200_OK'}
        # Service Account details
        # A service account is user identity that is associated with a service executable/ent. application.
        # E.g. SharePoint 2010 requires service accounts not only for its registered Windows services,
        # but also for its internal application components.
        # Options to select service account,
        #     A built-in operating system identity e.g. administrator, root etc or
        #     A local or domain user account e.g. padmakar, patil etc.
        # Note - System accounts are very highly privileged, so will create normal user account and assign permissions.
        # Also not that you can use user account as service account or create separate service account
        # for particular project/service. E.g. In demo project we are creating service account with
        # permission as is_staff, is_superuser (and used to create users during signup, reset password,
        # Activate/De-Activate user account.


class Signup(APIView):

    def create_user(self, username, password, email):
        self.email = email
        self.username = username
        self.password = password
        self.url = "http://localhost:5002/signup/"
        formdata = {'username': self.username, 'password': self.password, 'email':self.email}
        #data = formdata
        print("---In function, username, password, email's are --", self.username, self.password, self.email)
        # response = requests.get(url)
        #status = 200
        #return status

        response = requests.post(self.url, data=formdata)
        print("------First time execution", response.json(), response.status_code)
        try:
            response.raise_for_status()
            # Must have been a 200 status code
            # json_obj = response.json()
            # json_obj = {'data': response.json(), 'status_code': response.status_code, 'url': url}
            json_obj = {'data': response.json(), 'status_code': response.status_code}
            # print("--Return response --", json_obj)
            return json_obj
        except requests.exceptions.HTTPError as e:
            # Whoops it wasn't a 200
            # print("--Type of e --", type(e))
            # json_obj = {'data':response.json(), 'status_code': response.status_code, 'http_error_msg':e}
            json_obj = {'data': response.json(), 'status_code': response.status_code, 'url': self.url}
            # print("--Return response --", json_obj)
            return json_obj
            # eturn e
            # return "Error: " + str(e)

    def send_activation_mail(self, pk, username, email):
        self.pk = pk
        self.username = username
        self.email = email
        #self.token = token
        self.domain = "localhost:5002"
        user_activation_link = "http://localhost:5001/activate"

        #token = account_activation_token.make_token(user)
        msg = {
            'username': self.username,
            'id': self.pk,
            'domain': self.domain,
            'user_activation_link': user_activation_link
        }
        #ENCODING = 'utf-8'

        message_json = json.dumps(msg)
        message_data = base64.urlsafe_b64encode(message_json.encode('utf-8'))
        #message_base64 = b64encode(message_json.encode())

        #print("--msg-base64",message_base64)
        #message_urlsafe = urlsafe_b64decode(message_base64)
        #message_urlsafe = urlsafe_b64encode(message_base64)
        #message_urlsafe = urlsafe_b64encode(message_json)
        #print("---msg-url",message_urlsafe)
        message_string = urlsafe_b64decode(message_data)
        print("DECODE STRING: ", message_string)


        mail_subject = 'Activate your account.'
        message = render_to_string('acc_active_email.html', {
            'username': self.username,
            'id': self.pk,
            'id_b64' : message_data,
            'id_string': message_string,
            'domain': self.domain,
            'user_activation_link': user_activation_link
        })


        to_email = self.email
        email = EmailMessage( mail_subject, message, to=[to_email] )
        try:
            email.send()
            print("\n User info to activate account", username, pk)
            #return Response({'log_msg': 'Email send successfully.'}, status=status.HTTP_200_OK)
            return {'mail_status': 'Email send successfully.'}
        except:
            #return Response({'error_msg': 'Failed dependency to send mail'}, status=status.HTTP_424_FAILED_DEPENDENCY)
            return {'mail_status':'Failed dependency to send mail'}

    def post(self, request, format=None):
        path = request.path
        #print("---path--", path)
        form = UserCreationForm(request.data)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            print("---", username, password, email)
            # user = authenticate(request, username=username, password=password)
            #config = get_config('im_service')
            #im_url = config['data']['url_login']
            signup_user = self.create_user(username, password, email)
            print("--Type of signup_user output -", type(signup_user), signup_user)
            signup_status = signup_user['status_code']
            if signup_status == 201:
                msg = signup_user['data']['log_msg']
                id = signup_user['data']['id']
                username = signup_user['data']['username']
                email = signup_user['data']['email']
                group = 'users' # Default group name during signup

                # Get token
                jwt_token = JwtToken(username, group, email)
                token = jwt_token.get_token()
                print("-- TOKEN:", type(token),token)
                if token:
                    print("-- TOKEN:",token )

                # Send Registration mail
                """
                mail_status =''
                send_email = self.send_activation_mail(id, username, email)
                #if send_email:
                mail_status = send_email['mail_status']
                #else:
                print("--mail status", mail_status)
                """
                payload = {'log_msg': msg, 'id': id, 'username': username, 'email': email }
                print("---signup success --", payload)
                return Response(payload, status=status.HTTP_201_CREATED)


                """
                    # Following data used to send mail for account activation
                    pk = user_create.pk
                    username = user_create.username
                    current_site = get_current_site(request)
                    domain = current_site.domain
                    token = 'temptoken'
                    email = user_create.email
                    print("-data after creating user---",pk, username, current_site, domain, token, email)
                """
                """
                try:
                    self.send_activation_mail(username, pk, email, domain)
                    return Response(status=status.HTTP_201_CREATED)
                except:
                    print(" Error in sending mail.")
                    return Response(status=status.HTTP_424_FAILED_DEPENDENCY)
                """

            else:
                msg = signup_user['data']['error_msg']
                payload = {'error_msg': msg, 'username' :username }
                print("User creation fail")
                return Response(payload, status=status.HTTP_409_CONFLICT)
        else:
            return Response({"error": form.errors.as_json()}, status=400)

@api_view(['GET'])
# def activate(request, uidb64, token):
def activate(request, id):
    print("---received encoded parameter --",type(id), id)
    im_irl = "http://localhost:5002/activate"
    activate_id = im_irl + "/" + str(id) + "/"
    print("---IM url with id to activate account", activate_id)
    response = requests.post(activate_id)
    if response:
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
"""
@api_view(['GET'])
# def activate(request, uidb64, token):
def activate(request, id):
    print("---received encoded parameter --",type(id), id)
    #message_data = bytes(id, 'utf-8')
    #print("--bytes-", type(message_data), message_data)
    #id_string = str(id, 'utf-8')
    #ENCODING = 'utf-8'
    #message_data = bytearray(id)
    #message_data = str.encode(id)
    #message_data = id.decode('base64')
    #message_data = list(id)
    #message_data[0] = ''.join(message_data)
    #message_data = bytes(str.encode(id))
    #print("--after replacing first char b", type(message_data), message_data)

    #message_string = urlsafe_b64decode(message_data)
    #print("---message_string--", type(message_string), message_string)


    #data = str(id, 'utf-8')
    #print("---encoded data after converting to bytearray--", type(message_data), message_data)
    #message_string = id.base64.decode(ENCODING)
    #data = str(message_data, 'utf-8')
    #print("---conveting to str", data)
    #message_decode = urlsafe_b64decode(data)
    #print("---decoded data --", type(data), data)

    #message_string = urlsafe_b64decode(id)
    #print("---message_string--", type(message_string), message_string)
    #message_json = json.loads(message_string)
    #print("---message_json--", type(message_json), message_json)

    return Response(status=status.HTTP_200_OK)
"""


class Login(APIView):

    def check_authentication(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        formdata = {'username': self.username, 'password': self.password}
        data = formdata
        # print("---In function, url, username, password", self.url, self.username, self.password)
        # response = requests.get(url)
        response = requests.post(self.url, data=formdata)
        print("------First time execution", response.json(), response.status_code)
        try:
            response.raise_for_status()
            # Must have been a 200 status code
            # json_obj = response.json()
            # json_obj = {'data': response.json(), 'status_code': response.status_code, 'url': url}
            json_obj = {'data': response.json(), 'status_code': response.status_code}
            # print("--Return response --", json_obj)
            return json_obj
        except requests.exceptions.HTTPError as e:
            # Whoops it wasn't a 200
            # print("--Type of e --", type(e))
            # json_obj = {'data':response.json(), 'status_code': response.status_code, 'http_error_msg':e}
            json_obj = {'data': response.json(), 'status_code': response.status_code, 'url': url}
            # print("--Return response --", json_obj)
            return json_obj
            # eturn e
            # return "Error: " + str(e)

    def get_toekn(self, username):
        self.username = username
        token = {'username': self.username, 'token': 'dsfds)dfkdf_8j'}
        print("--Type of token--", type(token))
        return token

    def get_groups(self, username):
        self.username = username
        #groups = ['users', 'admins']
        groups = ['users']
        return groups

    def post(self, request, format=None):
        path = request.path
        #print("---path--", path)
        form = UserForm(request.data)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #formdata = {'username':username, 'password':password}
            #print("---username, password --", username, password)
            #user = authenticate(request, username=username, password=password)
            config = get_config('im_service')
            #config_url = config['url']
            #config_url = "http://localhost:5002/auth_login/"
            #url = config['data']['url_login']
            im_url = config['data']['url_login']
            #im_url = "http://localhost:5002/auth_login/"
            #print("---url --", im_url, config)
            #print("---Data received from get_config --", type(config), config)
            #print("--- url from get_config --", im_url)
            #print("--- static         url  --", im_url)

            #user = check_authentication(im_url, username, password)
            user = self.check_authentication(im_url, username, password)
            user_status = user['status_code']
            if user_status == 200:
                print("\n-- Type of user", type(user), user)
                username = user['data']['username']
                #group = 'users'
                group = self.get_groups(username)
                token = self.get_toekn(username)
                print("\n-- token --",type(token), token)

                payload = {'log_msg': "Authentication Successful.", 'username': username, 'group':group, 'token':token}
                request.session['group'] = payload['group']
                request.session['username'] = payload['username']
                return Response(payload,status=status.HTTP_200_OK)
            else:
                username = user['data']['username']
                payload = {"error_msg": "Your username and password didn't match. Please try again.", 'username': username}
                return Response(payload, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error": form.errors.as_json()}, status=400)


class Logout(APIView):
    pass

"""
def get_token():
    #response = requests.post(url='http://{}:{}/o/revoke_token/'.format(us_host, us_port), data=data)
    # Token service host name and port
    token_service_host_port = ["http://localhost", "5004"]
    token_service_base_url = ':'.join(token_service_host_port)
    get_token_path = [token_service_base_url, 'jwt/get_token/']
    url = '/'.join(get_token_path)
    print("-- Token Service url (to get token): ", url)

    return Response(status=status.HTTP_200_OK)
"""