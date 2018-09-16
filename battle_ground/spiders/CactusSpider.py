import codecs
import logging
import time

import requests
import simplejson


class Spider:
    _method = ''
    _url = ''

    def __init__(self, method, url):
        self._method = method
        self._url = url

    def request(self, params, headers, cookies):
        if self.is_duplicate(params):
            return
        time.sleep(3.6)
        prox = self.get_proxies()
        if self._method is 'get' or self._method is 'GET':
            r = requests.get(self._url, params=params, headers=headers, cookies=cookies, proxies=prox)
        elif self._method is 'post' or self._method is 'POST':
            r = requests.post(self._url, params=params, headers=headers, cookies=cookies, proxies=prox)
        else:
            r = requests.get(self._url, params=params, headers=headers, cookies=cookies, proxies=prox)
        temp = r.json()
        code, is_error = self.is_error(temp)
        logging.warn('errorcode %s is Error %s' % (code, is_error))
        if is_error:
            is_return = self.do_error(code)
            if is_return:
                return
        self.write_file(temp, params)
        return self.request_end(params, temp)

    def write_file(self, json, params):
        wfile = self.get_file_path(params)
        with codecs.open(wfile, 'w', 'utf-8') as wf:
            wf.write(simplejson.dumps(json, indent=2, sort_keys=True, ensure_ascii=False))
            wf.flush()

    def get_file_path(self, params):
        """
        get the target file path
        :return: return the write file path.
        """

    def is_duplicate(self, params):
        """
        is data duplicate
        :return: boolean
        """

    def request_end(self, params, data):
        """do something when request finished."""

    def is_error(self, data):
        """
        judge the request is success
        :param data: the response data
        :return: is error
        """

    def do_error(self, code):
        """
        do something when error
        :return: is give up when error
        """

    def get_proxies(self):
        """
        get network proxies
        :return: {

        }
        """
