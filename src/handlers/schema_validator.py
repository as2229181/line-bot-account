from common.exception import ValidationError


class SchemaValidator:
    @staticmethod
    def is_not_empty(data):
        if not data:
            message = "data could not be empty"
            raise ValidationError(message)
        return True
