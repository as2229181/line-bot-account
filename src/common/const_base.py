class ConstBase:
    """
    base class for const
    """

    _STR_FORMAT_TYPE = {"title", "upper", "lower"}

    _INVALID_TYPES = {
        classmethod,
        staticmethod,
        dict,
        list,
        set,
        tuple,
    }

    _DEFAULT_DELMITER = "_"
    _DEFAULT_FORMAT = "lower"

    _KEY_TO_VALUE_DICT: dict = {}
    _VALUE_TO_KEY_DICT: dict = {}
    _KEYS: list = []
    _VALUES: list = []

    @classmethod
    def get_values(cls):
        for k, v in cls.__dict__.items():
            if k.startswith("_") or type(v) in cls._INVALID_TYPES:
                continue
            cls._VALUES.append(v)
        return cls._VALUES

    @classmethod
    def value_to_key(cls, value):
        for k, v in cls.__dict__.items():
            if k.startswith("_") or type(v) in cls._INVALID_TYPES:
                continue
            if v == value:
                return k
        return None

    @classmethod
    def key_to_value(cls, key):
        for k, v in cls.__dict__.items():
            if k.startswith("_") or type(v) in cls._INVALID_TYPES:
                continue
            if k == key:
                return v
        return None

    @classmethod
    def to_dict(cls, reverse=False, fmt=None, delimiter=None):
        """
        class Status(ConstBase):
            NOT_STARTED = 1
            STARTED = 2
            COMPLETED = 3
        to_dict()
            -> {'NOT_STARTED': 1, 'STARTED': 2, 'COMPLETED': 3}

        to_dict(reverse=True, fmt='lower', delimiter= ' ')
            -> {1: 'not_started', 2: 'started, '3': 'completed'}
        """
        delimiter = delimiter or cls._DEFAULT_DELMITER

        if not isinstance(delimiter, str):
            raise ValueError(f"Invalid delimeter: {delimiter}")

        fmt = fmt or cls._DEFAULT_FORMAT
        if fmt.lower() not in cls._STR_FORMAT_TYPE:
            raise ValueError(f"Invalid format: {fmt}")
        result = set()
        for k, v in cls.__dict__.items():
            if k.startswith("_") or type(v) in cls._INVALID_TYPES:
                continue
            if "_" not in k or delimiter != "_":
                k.replace("_", delimiter)
            k = getattr(k, fmt.lower())()
            data = {v: k} if reverse else {k: v}
            result.update(data)
        return result
