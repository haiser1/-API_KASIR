class BaseResponse:
    def __init__(self):
        pass

    def response_success(self, code: int, status: str, data: dict):
        return {
            'code': code,
            'status': status,
            'data': data
        }

    def response_failed(self, code: int, status: str, message: str):
        return {
            'code': code,
            'status': status,
            'message': message
        }
