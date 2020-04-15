import enum

class HTTPCodes(enum.Enum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    NOT_FOUND = 404
    NOT_IMPLEMENTED = 501

    def getCode(self):
        return


