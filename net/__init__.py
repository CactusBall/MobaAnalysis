from urllib import parse


def get_openid_from_url(url):
    url_list = url.split('?')
    for test in url_list:
        if test.find('openid') == 0:
            return parse.parse_qs(test)['openid'][0]