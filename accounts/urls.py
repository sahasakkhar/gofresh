from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from accounts import views as accounts_view
from accounts.views import AccountViewSet, UserProfileViewSet

router = DefaultRouter()
# router.register(r'accounts', AccountViewSet)
router.register(r'user_profile', UserProfileViewSet)

urlpatterns = [

    url(r'^', include(router.urls)),
    url(r'^registration_email/$', accounts_view.registration_email, name='registration_email'),
    url(r'^registration_fb/$', accounts_view.registration_fb, name='registration_fb'),
    url(r'^obtain_auth_token/$', accounts_view.obtain_auth_token, name='obtain_auth_token'),
    url(r'^user_by_email/$', accounts_view.user_by_email, name='user_by_email'),

    url(r'^confirm_email/(?P<email_confirmation_key>[0-9a-zA-Z]+)/$', accounts_view.confirm_email,
        name='confirm_email'),
    url(r'^resend_confirmation_email/$', accounts_view.resend_confirmation_email, name='resend_confirmation_email'),

    url(r'^forgot_password_email/', accounts_view.forgot_password_email, name='forgot_password_email'),
    url(r'^forgot_password_form/(?P<password_reset_key>[0-9a-zA-Z]+)/$', accounts_view.forgot_password_form,
        name='forgot_password_form'),
    url(r'^forgot_password/(?P<password_reset_key>[0-9a-zA-Z]+)$', accounts_view.forgot_password,
        name='forgot_password'),
    url(r'^reset_password/$', accounts_view.reset_password, name='reset_password'),

    #url(r'^update_profile/$', accounts_view.update_profile, name='update_profile'),

    url(r'^terms_and_conditions/', accounts_view.terms_and_conditions, name='terms_and_conditions'),
    url(r'^privacy_policy/', accounts_view.privacy_policy, name='privacy_policy'),
    url(r'^buy_and_return_policy/', accounts_view.buy_and_return_policy, name='buy_and_return_policy'),

]
