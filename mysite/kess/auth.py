import typing
import json

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import re_path
from django.views.decorators.http import require_http_methods

from . import services
from .models import User


class CheckPasswordBackend:

    def authenticate(self, request=None, email=None, password=None) -> typing.Optional[User]:
        user = services.find_user_by_email(email=email)

        if user is None:
            return None

        if user.check_password(password):
            return user
        else:
            return None

    def get_user(self, user_id) -> typing.Optional[User]:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None


@require_http_methods(["POST"])
def login_view(request):
    body = json.loads(request.body.decode())
    user = authenticate(request, email=body["email"], password=body["password"])

    if user:
        login(request, user)
        return HttpResponse("OK")
    else:
        return HttpResponse("Unauthorized", status=401)

urlpatterns = [
    re_path("^login$", login_view),
]