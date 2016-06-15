import requests
from eva.conf import settings


class API(object):

    def __init__(self, url_prefix=None):
        if not url_prefix:
            url_prefix = settings.API_URL_PREFIX

        if url_prefix.endswith('/'):
            url_prefix = url_prefix[:-1]

        self.url_prefix = url_prefix

    def full_url(self, path):
        return self.url_prefix + path

    def get(self, path, **kwargs):
        return requests.get(self.full_url(path)).json()
