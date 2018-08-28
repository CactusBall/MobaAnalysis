import codecs
import os

import requests
import simplejson

import config
from config import duplicate, settings
from config.http import get_url, headers, cookies, pass_ticket
from net import get_openid_from_url


def _profile(profile_id):
    return 'profile_%s' % profile_id


def _openid(openid):
    return 'openid_%s' % openid


def _battle_info(game_seq):
    return 'battle_%s' % game_seq


def load_user_info(profile_id):
    if duplicate.is_user_profile_has(profile_id):
        return
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
    config.redis.hset()
    temp = r.json()
    errorcode = temp['errcode']
    if errorcode != 0:
        raise Exception
    wfile = os.path.join(settings.Res_UserInfo_Dir, '%s.txt' % _profile(profile_id))
    with codecs.open(wfile, 'w', 'utf-8') as wf:
        wf.write(simplejson.dumps(temp, indent=2, sort_keys=True, ensure_ascii=False))
    duplicate.record_profile(profile_id)
    game_list = temp['my_game']['game_list']
    for game in game_list:
        if game['app_name'] == '王者荣耀':
            jump_url = game['jump_url']
            return get_openid_from_url(jump_url)


def load_user_game_list(open_id):
    if duplicate.is_user_openid_has(open_id):
        return
    path = 'cgi-bin/gamewap/getusermobagameindex'
    url = get_url(path)
    params = {
        'openid': open_id,
        'key': '',
        'uid': '',
        'pass_ticket': pass_ticket
    }
    r = requests.get(url, params=params, headers=headers, cookies=cookies, verify=False)
    temp = r.json()
    error_code = temp['errcode']
    if error_code != 0:
        raise Exception
    wfile = os.path.join(settings.Res_Battle_List_Dir, '%s.txt' % _profile(open_id))
    with codecs.open(wfile, 'w', 'utf-8') as wf:
        wf.write(simplejson.dumps(temp, indent=2, sort_keys=True, ensure_ascii=False))
    duplicate.record_openid(open_id)
    battle_list = temp['battle_info']['battle_list']
    for battle in battle_list:
        game_seq = battle['game_seq']
        game_svr_entity = battle['game_svr_entity']
        relay_svr_entity = battle['relay_svr_entity']
        open_id = temp['user_info']['open_id']
        return game_seq, game_svr_entity, relay_svr_entity, open_id


def load_game_detail(game_seq, game_svr_entity, relay_svr_entity, open_id):
    if duplicate.is_battle_has(game_seq):
        return
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
    temp = r.json()
    error_code = temp['errcode']
    if error_code != 0:
        raise Exception
    wfile = os.path.join(settings.Res_Battle_Detail_Dir, '%s.txt' % _profile(game_seq))
    with codecs.open(wfile, 'w', 'utf-8') as wf:
        wf.write(simplejson.dumps(temp, indent=2, sort_keys=True, ensure_ascii=False))
    duplicate.record_game(game_seq)
