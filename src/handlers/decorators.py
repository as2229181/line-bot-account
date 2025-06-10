from functools import wraps
from flask import request
from common.exception import ValidationError


def payload_check(payload_field):
    def real_decorator(method, **kwargs):
        @wraps(method)
        def wrapper(*args, **kwargs):
            origin_paypload = request.get_json()
            new_payload = payload_field.validate(origin_paypload)
            if not new_payload:
                message = "payload is empty"
                raise ValidationError(message)
            return method(*args, **kwargs, payload=new_payload)

        return wrapper

    return real_decorator
