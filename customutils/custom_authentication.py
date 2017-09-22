from rest_framework.authtoken.models import Token

__author__ = 'goutom roy'

from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication, get_authorization_header


class AppTokenAuthentication(TokenAuthentication):

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'token':
            print('null token')
            return None

        if len(auth) == 1:

            msg = ('Invalid token header. No credentials provided.')
            print(msg)
            raise exceptions.AuthenticationFailed(msg)

        elif len(auth) > 2:

            msg = ('Invalid token header. Token string should not contain spaces.')
            print(msg)
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = ('Invalid token header. Token string should not contain invalid characters.')
            print(msg)
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        print('authenticate_credentials')
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            print('Invalid token.')
            raise exceptions.AuthenticationFailed(('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(('User inactive or deleted.'))
        return (token.user, token)