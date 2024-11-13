class BaseResponse:
    @staticmethod
    def response_success(code: int, status: str, data: any):
        return {
            'code': code,
            'status': status,
            'data': data
        }

    @staticmethod
    def response_failed(code: int, status: str, message: str):
        return {
            'code': code,
            'status': status,
            'message': message
        }
