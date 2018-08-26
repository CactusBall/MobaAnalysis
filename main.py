import requests
from urllib import parse

from config.http import get_url, cookies, headers, pass_ticket


def load_user_info(profile_id):
    path = 'cgi-bin/gamewap/getprofile2'
    url = get_url(path)
    params = {
        't': profile_id,
        'method': 'GET',
        'abtest_cookie': '',
        'abt': '27',
        'QB': ''
    }
    r = requests.get(url=url, params=params, headers=headers, cookies=cookies, verify=False)
    result = r.json()
    print(result)
    return result


def load_user_game_list(open_id):
    path = 'cgi-bin/gamewap/getusermobagameindex'
    url = get_url(path)
    params = {
        'openid': open_id,
        'key': '',
        'uid': '',
        'pass_ticket': pass_ticket
    }
    r = requests.get(url, params=params, headers=headers, cookies=cookies, verify=False)
    result = r.json()
    print(result)
    return result


def load_game_detail(game_seq, game_svr_entity, relay_svr_entity, open_id):
    path = '/cgi-bin/gamewap/getbattledetail'
    url = get_url(path)
    params = {
        'game_svr_entity': game_svr_entity,
        'game_seq': game_seq,
        'relay_svr_entity': relay_svr_entity,
        'openid': open_id,
        'uin': '',
        'key': '',
        'pass_ticket': pass_ticket
    }
    r = requests.get(url=url, params=params, headers=headers, cookies=cookies, verify=False)
    result = r.json()
    print(result)
    return result


def get_openid_from_url(url):
    url_list = url.split('?')
    for test in url_list:
        if test.find('openid') == 0:
            return parse.parse_qs(test)['openid'][0]


info = load_user_info('g1NlbysGi4KDI5aTA0V-65f9QlaA')
if info['errcode'] == 0:
    game_list = info['my_game']['game_list']
    for game in game_list:
        if game['app_name'] == '王者荣耀':
            jump_url = game['jump_url']
            openid = get_openid_from_url(jump_url)
            r = load_user_game_list(openid)
            print(r)

