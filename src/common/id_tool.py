from uuid import uuid4


class IDTool:
    @staticmethod
    def get_uuid():
        return uuid4()
