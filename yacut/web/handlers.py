import requests

from yacut.web.exceptions import APIError, PageNotFound


def get_short_url(request):
    data = requests.post('http://localhost/api/id/', json=request).json()
    if 'short_link' in data:
        return data['short_link']
    if 'message' in data:
        raise APIError(data['message'], user_input=request['url'],
                       status_code=400)
    raise APIError()


def get_original_url(url):
    data = requests.get('http://localhost/api/id/' + f'{url}/').json()
    if 'url' in data:
        return data['url']
    raise PageNotFound
