import codecs

import requests
import simplejson


class Spider:
    _method = ''

    def __init__(self, method):
        self.method = method

    def get(self, url, params):
        if self.is_duplicate():
            return
        if self._method is 'get':
            r = requests.get(url, params=params)
        elif self._method is 'post':
            r = requests.post(url, data=params)
        else:
            r = requests.get(url, params=params)
        temp = r.json()
        if self.is_error(temp):
            if self.do_error():
                return
        self.write_file(temp)
        self.request_end(temp)

    def write_file(self, json):
        wfile = self.get_file()
        with codecs.open(wfile, 'w', 'utf-8') as wf:
            wf.write(simplejson.dumps(json, indent=2, sort_keys=True, ensure_ascii=False))

    def get_file(self):
        """
        get the target file path
        :return: return the write file path.
        """

    def is_duplicate(self):
        """
        is data duplicate
        :return: boolean
        """

    def request_end(self, data):
        """do something when request finished."""

    def is_error(self, data):
        """
        judge the request is success
        :param data: the response data
        :return: is error
        """

    def do_error(self):
        """
        do something when error
        :return: is give up when error
        """
