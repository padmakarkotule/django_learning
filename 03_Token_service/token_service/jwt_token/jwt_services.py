# Jwt and oauth2
from base64 import b64decode, b64encode, urlsafe_b64decode, urlsafe_b64encode
import base64
import jwt
import json


class Jwt():

    def __init__(self, username):
        self.username = username
        #self.groups = groups
        #self.email = email
        #self._token_type = 'Bearer'
        _token_type = 'Bearer'
        # print("-- In Token Service:", self.username, self.groups, self.email)
        print("-- In Token Service:", self.username)

    def get_token(self, groups, email):
        # Other data
        client_id = 'Client_self'
        client_secret = 'Client_secret_self'
        # grant_type = 'password'
        # scope = 'read write',
        # expires_in = 300
        # token_type = 'Bearer',

        # Generate jwt token
        # 'token_type': token_type
        payload = payload = {
            'username': self.username,
            'groups': groups,
            'email': email,
            'client_id': client_id
        }

        SECRET = "JWT test token"
        # jwt_token = jwt.encode(payload, SECRET, algorithm='HS256')

        token = jwt.encode(payload, 'secret', 'HS256').decode('utf-8')
        print("\n--JWT:::GET_TOKEN: Org_JWT-TOKEN:", type(token), token)
        token = json.dumps(token)
        print("\n--JWT:::GET_TOKEN: AfterJsonDumps_JWT-TOKEN:", type(token), token)
        return token

    # Verify token
    def verify_token(self, token):
        # SECRET = "JWT test token"

        #user = request.data['username']
        user = self.username

        #header_info = request.META.get
        #received_token = request.META.get('HTTP_AUTHORIZATION')
        received_token = token
        print("\n-- JWT::VERIFY_TOKEN: Received token", user, type(received_token), received_token)
        received_token_json_loads = json.loads(received_token)
        print("\n-- JWT::VERIFY_TOKEN:: Received token after json load", user, type(received_token_json_loads), received_token_json_loads)

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
            print("\n--JWT::VERIFY_TOKEN: Data after decode:", username, groups, email, client_id)

            if user == username and user_group == groups:
                print("\n--JWT::VERIFY_TOKEN: username and group verification by JWT is success.")
                return {'log_msg': "Token verified."}
            else:
                print("\n--JWT::VERIFY_TOKEN: JWT token - encoded and decoded data mismatch")
                return False
        else:
            return {'error_msg': "Token mismatch", 'status': 'status.HTTP_401_UNAUTHORIZED'}


    # Class method
    @classmethod
    def class_method(cls):
        print("the class method was called")
    # Without even instantiating an object, we can access class methods as follows:
    # SomeClass.class_method()

