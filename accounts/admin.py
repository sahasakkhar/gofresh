from accounts.models import UserProfile, AuthUser, EmailConfirmationKey, PasswordResetKey
from django.contrib import admin
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import AuthUser, UserProfile
from rest_framework.authtoken.models import Token


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = AuthUser
        fields = ('email', 'user_type', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            AuthUser.objects.get(email=email)
            raise forms.ValidationError('Email already taken')
        except AuthUser.DoesNotExist:
            return email

    def clean_password1(self):

        password1 = self.cleaned_data.get("password1")
        import re
        match_result = re.match(r'^[0-9A-Za-z_-]*$', password1)

        if len(password1) < 6:
            raise forms.ValidationError(['Password too short! Minimum 6 characters long.'])

        elif len(password1) > 30:
            raise forms.ValidationError(['Password too long! Maximum 30 characters long.'])

        elif match_result is None:
            raise forms.ValidationError(
                ['Only alphanumeric(a-zA-Z0-9) and' + "' - ', " + "'_'" + ' characters are allowed.'])

        return password1

    def clean_password2(self):

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.is_active = True
        user.set_password(self.cleaned_data["password1"])
        user.save()
        Token.objects.create(user=user)
        UserProfile.objects.create(auth_user=user, is_active=True)
        return user

    """
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        print("commit : %s" % commit)
        if commit:
            user.save()
            Token.objects.create(user=user)
            UserProfile.objects.create(auth_user=user)
        return user
    """

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = AuthUser
        fields = ('is_active', 'user_type')


class AuthUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    readonly_fields = ('id', 'date_added',)
    list_display = ('email', 'user_type', 'is_active',)
    list_filter = ('email',)
    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = [
        (None, {'fields': ('id', 'email', 'password',)}
         ),

        ('Permissions', {'fields': ['is_active', 'is_superuser', 'user_type', 'groups', 'user_permissions'],
                         'classes': ['collapse']
                         }
         ),

        ('Important dates', {'fields': ('date_added',)}
         )
    ]

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_type', 'password1', 'password2')}
         ),
    )


class CustomFollowerChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.first_name


class CustomFollowerForm(forms.ModelForm):
    user_profile_first_name = CustomFollowerChoiceField(queryset=UserProfile.objects.all())

    class Meta:
        model = UserProfile
        fields = ['user_profile_first_name', ]


class UserProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'date_added', 'updated')
    list_display = ('id', 'auth_user', 'date_added', 'updated', 'is_active')
    list_filter = ('name', 'auth_user__email', 'is_active')
    list_display_links = ('auth_user',)
    search_fields = ('auth_user__email', 'name',)


class EmailConfirmationKeyAdmin(admin.ModelAdmin):
    list_display = ('auth_user', 'key',)
    search_fields = ('auth_user__email',)


admin.site.register(AuthUser, AuthUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(PasswordResetKey)
admin.site.register(EmailConfirmationKey, EmailConfirmationKeyAdmin)
