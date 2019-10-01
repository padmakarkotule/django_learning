# Jwt and oauth2
from base64 import b64decode, b64encode, urlsafe_b64decode, urlsafe_b64encode
import base64
import jwt
import json


class JwtGetToken():

    def __init__(self, username, groups, email):
        self.username = username
        self.groups = groups
        self.email = email
        self._token_type = 'Bearer'
        print("-- In Token Service:", self.username, self.groups, self.email)

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
            'username': username,
            'groups': groups,
            'email': email,
            'client_id': client_id
        }

        SECRET = "JWT test token"
        # jwt_token = jwt.encode(payload, SECRET, algorithm='HS256')

        jwt_token = jwt.encode(payload, 'secret', 'HS256').decode('utf-8')
        print("\n Org_JWT-TOKEN:", jwt_token)
        jwt_token = json.dumps(jwt_token)
        print("\n-- AfterJsonDumps_JWT-TOKEN:", type(jwt_token), jwt_token)

        return self.jwt_token
