from urllib import parse


def get_openid_from_url(url):
    url_list = url.split('?')
    for param in url_list:
        if param.find('openid') == 0:
            return parse.parse_qs(param)['openid'][0]


def get_profileid_from_url(url):
    url_list = url.split('?')
    for param in url_list:
        if param.find('t') == 0:
            return parse.parse_qs(param)['t'][0]
