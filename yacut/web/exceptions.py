ERROR_MESSAGE = 'Ошибка сервера'


class DBError(Exception):

    def __init__(self, form, message=ERROR_MESSAGE, status_code=500, ):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.form = form


class PageNotFound(Exception):
    pass
