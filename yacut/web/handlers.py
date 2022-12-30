from yacut.models import URLMap
from yacut.web.exceptions import DBError, PageNotFound
from yacut.web.forms import URLForm


def get_short_url(form: URLForm):
    try:
        return URLMap.make_short_url(
            form.original_link.data,
            form.custom_id.data
        )
    except URLMap.DBError as error:
        raise DBError(form, error, 400)


def get_original_url(url):
    original_url = URLMap.get_original_url(url)
    if original_url:
        return original_url
    raise PageNotFound()
