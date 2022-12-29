ERROR_MESSAGE = 'Ошибка сервера'


class APIError(Exception):

    def __init__(self, message=ERROR_MESSAGE,
                 status_code=500, user_input=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.user_input = user_input


class PageNotFound(Exception):
    pass
