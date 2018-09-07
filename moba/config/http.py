from config.settings import key, pass_ticket, uin, pgv_pvid, sd_cookie_crttime, sd_userid, host, accept, ua, \
    accept_lang, referer, accept_encoding

cookies = {
    'key': key,
    'pass_ticket': pass_ticket,
    'uin': uin,
    'pgv_pvid': pgv_pvid,
    'sd_cookie_crttime': sd_cookie_crttime,
    'sd_userid': sd_userid
}

headers = {
    'Host': host,
    'Accept': accept,
    'Connecttion': 'keep-alive',
    'User-Agent': ua,
    'Accept-Language': accept_lang,
    'Referer': referer,
    'Accept-Encoding': accept_encoding
}


def get_url(path):
    return 'https://%s/%s' % (host, path)
