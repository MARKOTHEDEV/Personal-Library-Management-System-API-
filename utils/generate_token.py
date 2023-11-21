
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model


User = get_user_model()

def update_login(refresh):
    data = dict()
    data["refresh"] = str(refresh)
    data["access"] = str(refresh.access_token)

    return data


def gen_token(user: User):
    token = RefreshToken.for_user(user)
    token["email"] = user.email
    token["first_name"] = user.first_name
    token["last_name"] = user.last_name
    token["full_name"] = user.full_name

    return token
