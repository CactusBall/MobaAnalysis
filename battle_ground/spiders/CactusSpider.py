import codecs

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
        prox = self.get_proxies()
        if self._method is 'get' or self._method is 'GET':
            r = requests.get(self._url, params=params, headers=headers, cookies=cookies, proxies=prox, verify=False)
        elif self._method is 'post' or self._method is 'POST':
            r = requests.post(self._url, params=params, headers=headers, cookies=cookies, proxies=prox)
        else:
            r = requests.get(self._url, params=params, headers=headers, cookies=cookies, proxies=prox)
        temp = r.json()
        code, is_error = self.is_error(temp)
        if is_error:
            if self.do_error(code):
                return
        self.write_file(temp, params)
        print(params)
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
