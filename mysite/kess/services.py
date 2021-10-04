import datetime
import typing

from .models import User


def create_user(email: str, name: str, points: int, creation_date: datetime.datetime, password: str) -> User:
    return User.objects.create_user(email=email,
                                    name=name,
                                    points=points,
                                    creation_date=creation_date,
                                    password=password)


def create_superuser(email: str, name: str, points: int, creation_date: datetime.datetime, password: str) -> User:
    return User.objects.create_superuser(email=email,
                                         name=name,
                                         points=points,
                                         creation_date=creation_date,
                                         password=password)


def find_user_by_email(email: str) -> typing.Optional[User]:
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None
