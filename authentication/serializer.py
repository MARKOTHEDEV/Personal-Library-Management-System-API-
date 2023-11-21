from rest_framework import serializers
from .models import User
from utils.exception import CustomValidation
from rest_framework import status

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