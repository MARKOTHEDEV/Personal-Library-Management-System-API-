from rest_framework import serializers
from .models import User
from utils.exception import CustomValidation
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model,authenticate,user_logged_in
from rest_framework.exceptions import AuthenticationFailed
from utils.generate_token import update_login,gen_token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings


class RegisterUserSerializers(serializers.Serializer):
    password = serializers.CharField(trim_whitespace=True,write_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = User
        fields  = ["first_name","last_name","email","password"]

    def validate(self, attrs):
        'do a little bit of check'
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            raise CustomValidation(detail='User already exits',status_code=status.HTTP_400_BAD_REQUEST)
        return super().validate(attrs)

    def create(self, validated_data):
        'create the user'
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        user = User.objects.create_user(email=email,password=password,**validated_data)
        return user
    

class LoginSerializer(TokenObtainPairSerializer):

    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={"input_type": "password"}, trim_whitespace=False,write_only=True)

    def validate(self, attrs):
        USER_MODEL= get_user_model()
        email = attrs.get("email", None)
        password = attrs.get("password", None)
        request = self.context.get("request", None)
        try:
            user = USER_MODEL.objects.get(email=email)
        except USER_MODEL.DoesNotExist:
            user = None
        auth_user = authenticate(username=email, password=password)

        
        if (not user and not auth_user) or (user.is_active and not auth_user):
            raise AuthenticationFailed(
                "Invalid credentials, username or password incorrect"
            )
        if user.is_active  == False:
            raise AuthenticationFailed(
                "Please check your mail for activation token"
            )

        refresh = self.get_token(user)
        user_login = update_login(refresh)
        # user_logged_in.send(sender=user.__class__, request=request, user=user)
        return user_login
    


    
    @classmethod
    def get_token(cls, user):
        """
        get the token for a user
        Args:
            user:
        Returns:
        """
        token = gen_token(user)

        return token
    


class CustomTokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


    def validate(self, attrs):
        refresh = attrs.get("refresh_token")
        if refresh is None:
            raise AuthenticationFailed(
                "Authentication Credentials were not provided"
            )
        try:
            refresh = RefreshToken(refresh)
        except TokenError as e:
            raise AuthenticationFailed(str(e))
        
        data = {"access": str(refresh.access_token)}
        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data["refresh"] = str(refresh)

        return data