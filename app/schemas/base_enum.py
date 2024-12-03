import enum

class BaseEnum(enum.Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))