from django.apps import AppConfig


class JwtTokenConfig(AppConfig):
    name = 'jwt_token'
    verbose_name = "JWT Token"

class Oauth2TokenConfig(AppConfig):
    name = 'oauth2_token'
    verbose_name = "Oauth2 Token"
