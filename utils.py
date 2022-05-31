import hashlib

from flask import request, current_app
from flask_restx import abort

import base64
from datetime import datetime, timedelta

import constants
import jwt


def get_hashed_password(password: str):
    hashed_password: bytes = hashlib.pbkdf2_hmac(
        hash_name=constants.HASH_NAME,
        salt=constants.HASH_SALT.encode("utf-8"),
        iterations=constants.HASH_GEN_ITERATIONS,
        password=password.encode("utf-8")
    )
    return base64.b64encode(hashed_password).decode("utf-8")


def generate_tokens(data: dict):
    data["exp"] = datetime.utcnow() + timedelta(minutes=30)
    data["refresh_token"] = False

    access_token = jwt.encode(
        payload=data,
        key=constants.SECRET_HERE,
        algorithm=constants.JWT_ALGORITHM,
    )

    data["exp"] = datetime.utcnow() + timedelta(days=30)
    data["refresh_token"] = True

    refresh_token = jwt.encode(
        payload=data,
        key=constants.SECRET_HERE,
        algorithm=constants.JWT_ALGORITHM,
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


def get_token_from_headers(headers: dict):
    # Получаем заголовок с токеном из запроса:
    if "Authorization" not in request.headers:
        abort(401)

    return headers["Authorization"].split(" ")[-1]


def decode_token(token: str, refresh_token: bool = False):
    decoded_token = {}
    # Пытаемся раскодировать токен
    try:
        decoded_token = jwt.decode(
            jwt=token,
            key=constants.SECRET_HERE,
            algorithms=[constants.JWT_ALGORITHM]
        )
    except jwt.PyJWTError as e:
        current_app.logger.info("Got wrong token", token)
        abort(401)

    # Проверяем, что это не refresh_token

    if decoded_token["refresh_token"] != refresh_token:
        abort(400, message="Got wrong token type")

    return decoded_token


def auth_required(func):
    def wrapper(*args, **kwargs):
        # Получаем заголовок с токеном из запроса:
        token = get_token_from_headers(request.headers)
        # Пытаемся раскодировать токен
        decoded_token = decode_token(token)

        return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        # Получаем заголовок с токеном из запроса:
        token = get_token_from_headers(request.headers)

        # Пытаемся раскодировать токен
        decoded_token = decode_token(token)

        if decoded_token["role"] != "admin":
            abort(403)

        return func(*args, **kwargs)
    return wrapper
