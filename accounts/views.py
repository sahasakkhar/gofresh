from rest_framework.parsers import FormParser, MultiPartParser

from customutils.custom_authentication import AppTokenAuthentication
from customutils.custom_validators import is_email_address_valid, validate_password
from customutils.emailtasks import SendAccountVerificationEmail, ForgotPasswordEmail
from customutils.method_box import get_confirmation_email_subject_message, \
    get_forget_password_email_subject_message, create_email_confirm_key, create_password_reset_key
from accounts.models import AuthUser, EmailConfirmationKey, UserProfile, PasswordResetKey
from accounts.serializers import UserSerializer, UserProfileSerializer, UserPostSerializer
from django.contrib.auth.models import AnonymousUser
from customutils.full_scope_static import GENERAL_USER
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, parser_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from accounts.tasks import account_confirmation_email, forgot_password_email_send
from gofresh.settings import get_running_host


@api_view(['POST'])
@renderer_classes((JSONRenderer,))
def registration_fb(request):
    email = request.data.get('email')
    name = request.data.get('name')
    gender = request.data.get('gender')
    date_of_birth = request.data.get('date_of_birth')
    fb_access_token = request.data.get('fb_access_token')
    fb_uid = request.data.get('fb_uid')

    data = {}

    try:
        auth_user = AuthUser.objects.get(email=email)
        user_profile = UserProfile.objects.get(auth_user=auth_user)

        if user_profile.is_logged_in_from_fb is False:
            data['message'] = 'this email was previously used for email login.'
            return Response(data=data, status=status.HTTP_409_CONFLICT)
        else:
            data = get_user_info(auth_user, request)
            return Response(data=data, status=status.HTTP_200_OK)

    except AuthUser.DoesNotExist:

        user = AuthUser(email=email, user_type=GENERAL_USER)
        user.set_password('gogogofresh')
        user.is_active = True
        user.save()

        user_profile = UserProfile(auth_user=user)
        user_profile.name = name
        user_profile.gender = gender
        user_profile.date_of_birth = date_of_birth
        user_profile.is_logged_in_from_fb = True
        user_profile.fb_access_token = fb_access_token
        user_profile.fb_uid = fb_uid
        user_profile.is_active = True
        user_profile.save()

        Token.objects.create(user=user)
        data = get_user_info(user, request)

        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
@renderer_classes((JSONRenderer,))
@parser_classes((FormParser, MultiPartParser,))
def registration_email(request):
    print('aise')

    email = request.data.get('email')
    name = request.data.get('name')
    image = request.data.get('image')
    phone = request.data.get('phone')
    # phone_optional = request.POST.get('phone_optional')
    #gender = request.POST.get('gender')
    #date_of_birth = request.POST.get('date_of_birth')
    password = request.POST.get('password')

    data = {}
    if not is_email_address_valid(email):
        data['email'] = 'This is not a valid email address.'

    msg = validate_password(password)
    if msg is not None:
        data['password'] = msg

    if len(data) > 0:
        return Response(data=data, status=status.HTTP_406_NOT_ACCEPTABLE)

    try:
        auth_user = AuthUser.objects.get(email=email)
        user_profile = UserProfile.objects.get(auth_user=auth_user)

        if user_profile.is_logged_in_from_fb is True:
            data['message'] = 'this email was previously used for facebook login.'
            return Response(data=data, status=status.HTTP_409_CONFLICT)
        else:
            data['message'] = 'email address already taken.'
            return Response(data=data, status=status.HTTP_409_CONFLICT)

    except AuthUser.DoesNotExist:

        auth_user = AuthUser(email=email, user_type=GENERAL_USER)
        auth_user.set_password(password)
        auth_user.save()
        Token.objects.create(user=auth_user)

        user_profile = UserProfile(auth_user=auth_user)
        user_profile.name = name
        #print(image.name)
        if image is not None:
            user_profile.image.save(image.name, image)

        #user_profile.date_of_birth = date_of_birth
        user_profile.phone = phone
        # user_profile.phone_optional = phone_optional
        user_profile.save()

        '''
        from accounts.views import get_confirmation_email_subject_message
        subject, message = get_confirmation_email_subject_message(user)
        user.email_user(subject, message)

        '''

        email_confirmation_key = create_email_confirm_key(auth_user)
        #account_confirmation_email.delay(name, email, email_confirmation_key)
        email_thread = SendAccountVerificationEmail(name, email, email_confirmation_key)
        email_thread.start()

        data = get_user_info(auth_user, request)
        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
@renderer_classes((JSONRenderer,))
def obtain_auth_token(request):
    print('obtain_auth_token')
    email = request.POST.get('email')
    password = request.POST.get('password')
    print('email : %s password : %s' % (email, password))

    if is_email_address_valid(email):
        try:
            user = AuthUser.objects.get(email=email)
            if user.check_password(password):
                data = get_user_info(user, request)
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                data = {'message': 'Password does not match with email.'}
                return Response(data=data, status=status.HTTP_406_NOT_ACCEPTABLE)

        except AuthUser.DoesNotExist:
            data = {'message': 'No user found with given email.'}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    else:
        data = {'message': 'This is not a valid email address.'}
        return Response(data=data, status=status.HTTP_205_RESET_CONTENT)


def get_user_info(user, request):
    data = {}
    token = Token.objects.get(user=user)
    data['token'] = token.key
    profile = UserProfile.objects.get(auth_user=user)
    profile_serializer = UserProfileSerializer(profile, context={"request": request})
    data['profile'] = profile_serializer.data

    return data

    """
    After confirming email user will be active means user got write access.
    * user active means he has read and write access
    * user not active means he has only read access
    """


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def confirm_email(request, email_confirmation_key):
    try:
        eck = EmailConfirmationKey.objects.get(key=email_confirmation_key)
        eck.auth_user.is_active = True
        eck.auth_user.save()
        user_profile = UserProfile.objects.get(auth_user=eck.auth_user)
        user_profile.is_active = True
        user_profile.save()

        eck_list = EmailConfirmationKey.objects.filter(auth_user=eck.auth_user)
        for each_eck in eck_list:
            each_eck.delete()

        data = {'message': 'email confirmed.'}
        return Response(data=data, status=status.HTTP_200_OK)

    except EmailConfirmationKey.DoesNotExist:
        data = {'message': 'invalid email confirmation key'}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    """
    * User can login even he is not confirmed his email yet.
    * After login user will be shown a "Resend confirmation email" button in home screen if not confirmed yet.
    * Only logged in user can send confirmation email again.
"""


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
@authentication_classes((AppTokenAuthentication,))
def resend_confirmation_email(request):
    if isinstance(request.user, AnonymousUser):
        error_message = {'error_message': 'you are not authorized to access this functionality.'}
        return Response(data=error_message, status=status.HTTP_401_UNAUTHORIZED)

    subject, message = get_confirmation_email_subject_message(request.user)
    if request.user.email_user(subject, message):
        print('email sent successfully.')
        data = {'message': 'confirmation email sent'}
        return Response(data=data, status=status.HTTP_200_OK)
    else:
        print('email did not sent.')
        data = {'message': 'confirmation email was not sent.Check you email address and resend'}
        return Response(data=data, status=status.HTTP_200_OK)


"""
    * This method will be used after getting sure that
    a user is present in the database with given email.
    * Use 'user_by_email' method to be sure that a user with given email is there.
"""


@api_view(['POST'])
@renderer_classes((JSONRenderer,))
def forgot_password_email(request):

    user = AuthUser.objects.get(email=request.POST.get('email'))
    user_profile = UserProfile.objects.get(auth_user=user)

    password_reset_key = create_password_reset_key(user)
    password_reset_link = get_running_host() + "/forgot_password_form/" + password_reset_key + "/"

    fpe = ForgotPasswordEmail(user_profile.name, user.email, password_reset_link)
    fpe.start()

    data = {'message': 'forget password email sent'}
    return Response(data=data, status=status.HTTP_200_OK)


"""
will be clicked from email
"""

@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,))
def forgot_password_form(request, password_reset_key):
    try:
        prk = PasswordResetKey.objects.get(key=password_reset_key)
        data = {'password_reset_key': prk.key}
        return Response(data=data, status=status.HTTP_200_OK, template_name='accounts/password_reset_form.html')

    except PasswordResetKey.DoesNotExist:
        data = {'error_message': 'invalid password reset key'}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST,
                        template_name='accounts/invalid_password_reset_key.html')


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,))
def landing_page(request):
    data = {'error_message': 'invalid password reset key'}
    return Response(data=data, status=status.HTTP_200_OK, template_name='accounts/landing_page.html')


"""
 * This method will be called from password reset form. when user clicks submit.
"""


@api_view(['POST'])
@renderer_classes((JSONRenderer,))
def forgot_password(request, password_reset_key):

    password = request.POST.get('password')
    repeat_password = request.POST.get('repeat_password')

    if password != repeat_password:
        data = {'error_message': 'password and repeat-password does not match.'}
        return Response(data=data, status=status.HTTP_205_RESET_CONTENT)
    try:
        prk = PasswordResetKey.objects.get(key=password_reset_key)
        prk.auth_user.set_password(password)
        prk.auth_user.save()
        prk_list = PasswordResetKey.objects.filter(auth_user=prk.auth_user)
        for each_prk in prk_list:
            each_prk.delete()
        data = {'message': 'Password saved successfully.'}
        return Response(data=data, status=status.HTTP_200_OK)
    except PasswordResetKey.DoesNotExist:
        data = {'error_message': 'Invalid action'}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


"""
    * Logged in user will reset his password with this full_scope_api
"""


@api_view(['POST'])
@renderer_classes((JSONRenderer,))
@authentication_classes((AppTokenAuthentication,))
def reset_password(request):
    if isinstance(request.user, AnonymousUser):
        data = {'error_message': 'You are not authorized to access this password reset functionality!'}
        return Response(data=data, status=status.HTTP_200_OK)

    # credential included as post data
    current_password = request.POST.get('current_password')
    new_password = request.POST.get('new_password')

    # credential included in header
    # current_password = request.META.get('current_password', None)
    # new_password = request.META.get('new_password', None)

    user = AuthUser.objects.get(email=request.user.email)
    if user.check_password(current_password):
        user.save_password(new_password)
        user.save()
        data = {'message': 'Password saved successfully.'}
        return Response(data=data, status=status.HTTP_200_OK)
    else:
        data = {'message': 'Current password does not match.'}
        return Response(data=data, status=status.HTTP_200_OK)


"""
    * This method returns user's public profile.
"""


@api_view(['POST'])
@renderer_classes((JSONRenderer,))
def user_by_email(request):
    email = request.POST.get('email')

    if is_email_address_valid(email):
        try:
            auth_user = AuthUser.objects.get(email=email)
            user_profile = UserProfile.objects.get(auth_user=auth_user)

            if user_profile.is_logged_in_from_fb is True:
                data = {'message': 'this email was previously used for facebook login.'}
                return Response(data=data, status=status.HTTP_409_CONFLICT)
            else:
                data = get_user_info(auth_user, request)
                return Response(data=data, status=status.HTTP_200_OK)

        except AuthUser.DoesNotExist:
            data = {'message': 'No user found with given email address.'}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    else:
        data = {'message': 'This is not a valid email address.'}
        return Response(data=data, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,))
def terms_and_conditions(request):
    return Response(status=status.HTTP_200_OK, template_name='accounts/terms_and_conditions.html')


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,))
def privacy_policy(request):
    return Response(status=status.HTTP_200_OK, template_name='accounts/privacy_policy.html')


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,))
def buy_and_return_policy(request):
    return Response(status=status.HTTP_200_OK, template_name='accounts/buy_and_return_policy.html')


class AccountViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = AuthUser.objects.all()

    def get_serializer_class(self):

        serializers = {
            'list': UserSerializer,
            'create': UserPostSerializer,
            'retrieve': UserSerializer,
            'update': UserSerializer,
            'destroy': UserSerializer,
            'partial_update': UserSerializer,
            'default': None,
        }
        return serializers.get(self.action, serializers['default'])

    def list(self, request, *args, **kwargs):

        if isinstance(request.user, AuthUser) and request.user.user_type == 1:
            users = AuthUser.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif isinstance(request.user, AnonymousUser):
            users = AuthUser.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            data = {'error_message': 'you are not authorized to access this information'}
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, *args, **kwargs):

        if isinstance(request.user, AnonymousUser):
            data = {'error_message': 'you are not authorized to access this information'}
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.user.id == int(kwargs.get('pk')):
            serializer = UserSerializer(request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        elif request.user.user_type == 1:
            serializer = UserSerializer(request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:
            data = {'error_message': 'you are not authorized to access this information'}
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, *args, **kwargs):

        """
        Anonymous or admin can create a new user.
    """
        if isinstance(request.user, AnonymousUser) or (request.user.user_type == 1):
            serializer = UserPostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = {'success_message': 'User created successfully.'}
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = UserProfile.objects.all()
    lookup_field = 'pk'

    def get_serializer_class(self):
        serializers = {
            'list': UserProfileSerializer,
            'create': UserProfileSerializer,
            'retrieve': UserProfileSerializer,
            'update': UserProfileSerializer,
            'destroy': UserProfileSerializer,
            'partial_update': UserProfileSerializer,
            'default': UserProfileSerializer,
        }
        return serializers.get(self.action, serializers['default'])

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
