import enum


class OutputType(enum.Enum):
    NET = '!N'
    HOST = '!H'
    PROHIB = '!X'
    SUCCESS = 'OK'
    ERROR = 'ERROR'
