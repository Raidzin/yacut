from yacut.api.utils import process_data, get_original_url
from yacut.api.exceptions import ValidationError
from yacut.web.forms import URLForm
from yacut.web.exceptions import APIError, PageNotFound

"""
Тут планировалось сделать запросы к api через requests.
Хотелось так сделать для того, чтоб реализовать распределённую архитектуру,
апи отдельно, фронт отдельно. Но тесты так сделать не позволили,
поэтому приходится импортировать функции из api,
что архитектурно не очень хорошо(
"""


def get_short_url(form: URLForm):
    try:
        data = process_data({
            'url': form.original_link.data,
            'custom_id': form.custom_id.data,
        })
        return data['short_link']
    except ValidationError as error:
        raise APIError(
            form=form,
            message=error.message,
            status_code=error.status_code
        )


def get_original_url_web(url):
    try:
        return get_original_url(url)
    except ValidationError:
        raise PageNotFound()