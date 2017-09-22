from rest_framework import serializers
from accounts.models import AuthUser, UserProfile, EmailConfirmationKey


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AuthUser
        fields = ('id', 'email', 'user_type', 'date_added', 'updated', 'is_active')


class UserProfileSerializer(serializers.ModelSerializer):
    auth_user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ('auth_user', 
            'id', 
            'name',
            'image',
            'width_field',
            'height_field',
            'date_of_birth', 
            'phone',
            'phone_optional', 
            'gender',
            'is_logged_in_from_fb',
            'fb_access_token',
            'fb_uid', 
            'date_added',
            'updated',
            'is_active')


class UserPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthUser
        fields = ('email', 'password', 'user_type', )

    def create(self, validated_data):
        user = AuthUser(email=validated_data['email'], user_type=validated_data['user_type'])
        user.set_password(validated_data['password'])
        user.save()
        return user


    def validate_password(self, password):
        """
        Validate Password.
        default password model length validation :
        1-128

        default empty error message:
        "field": ["This field may not be blank."],
        """
        import re
        match_result = re.match(r'^[0-9A-Za-z_-]*$', password)
        #Use at least 6 to 30 characters
        if len(password) < 6:
            raise serializers.ValidationError(['Password too short! Minimum 6 characters long.'])

        elif len(password) > 30:
            raise serializers.ValidationError(['Password too long! Maximum 30 characters long.'])

        elif match_result is None:
            raise serializers.ValidationError(['Only alphanumeric(a-zA-Z0-9) and' + "' - ', " + "'_'" +' characters are allowed.'])


        return password


class EmailConfirmationKeySerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailConfirmationKey
        fields = '__all__'

