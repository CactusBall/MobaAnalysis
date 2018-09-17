import codecs
import logging
import os
import time

import requests
import simplejson

from config import duplicate, settings
from config.http import get_url, headers, cookies, pass_ticket
from net import get_openid_from_url, get_profileid_from_url
from net.proxies import deprecate_big_ip


def _profile(profile_id):
    return 'profile_%s' % profile_id


def _openid(openid):
    return 'openid_%s' % openid


def _battle_info(game_seq):
    return 'battle_%s' % game_seq


def load_user_info(profile_id, prox, ip):
    if duplicate.is_user_profile_has(profile_id):
        logging.warn('duplicate load_user_info')
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
    r = requests.get(url=url, params=params, headers=headers, cookies=cookies, proxies=prox)
    temp = r.json()
    error_code = temp['errcode']
    logging.warn('load_user_info errorcode %s ip is %s' % (error_code, ip))
    if error_code != 0:
        raise Exception
    wfile = os.path.join(settings.Res_UserInfo_Dir, '%s.txt' % _profile(profile_id))
    with codecs.open(wfile, 'w', 'utf-8') as wf:
        wf.write(simplejson.dumps(temp, indent=2, sort_keys=True, ensure_ascii=False))
    if error_code == 0:
        duplicate.record_profile(profile_id)
    game_list = temp['my_game']['game_list']
    for game in game_list:
        if game['app_name'] == '王者荣耀':
            jump_url = game['jump_url']
            return error_code, get_openid_from_url(jump_url)


def load_zone_area_id(open_id, prox, ip):
    if duplicate.is_zone_has(open_id):
        logging.warn('duplicate load_zone_area_id')
        return
    # time.sleep(random.randrange(7, 8))
    time.sleep(1.8)
    path = 'cgi-bin/gamewap/getusermobagameindex'
    url = get_url(path)

    params = {
        'openid': open_id,
        'key': '',
        'uid': '',
        'pass_ticket': pass_ticket,
        'QB': ''
    }
    headers['Referer'] = 'https://game.weixin.qq.com/cgi-bin/h5/static/smobadynamic/dynamic.html?opexnid=' + open_id + '&ssid=3101&abt=27&rpt_allpath=3101&abtest_cookie=BAABAAoACwASABMABAAjlx4AV5keAGmZHgBsmR4AAAA%ds3D&pass_ticket=' + pass_ticket + '&wx_header=1'
    r = requests.get(url, params=params, headers=headers, cookies=cookies, proxies=prox)
    temp = r.json()
    error_code = temp['errcode']
    logging.warn('load_zone_area_id errorcode %s ip is %s' % (error_code, ip))
    if error_code == 40001:
        time.sleep(60 * 60 * 24)
    if error_code == 45009:
        # time.sleep(61)
        deprecate_big_ip(ip)
    if error_code != 0:
        raise Exception
    wfile = os.path.join(settings.Res_Game_Index_Dir, '%s.txt' % _profile(open_id))
    with codecs.open(wfile, 'w', 'utf-8') as wf:
        wf.write(simplejson.dumps(temp, indent=2, sort_keys=True, ensure_ascii=False))
    duplicate.record_zone(open_id)
    zone_area_id = temp['user_info']['zone_area_id']
    return error_code, zone_area_id, open_id


def load_user_game_list(open_id, offset, zone_area_id, prox, ip):
    if duplicate.is_user_openid_has(open_id) and offset == 0:
        logging.warn('duplicate load_user_game_list %s' % open_id)
        return
    limit = 10
    # time.sleep(random.randrange(3, 4))
    time.sleep(3)
    path = 'cgi-bin/gamewap/getusermobabattleinfolist'
    url = get_url(path)

    params = {
        'openid': open_id,
        'key': '',
        'uid': '',
        'pass_ticket': pass_ticket,
        'offset': offset,
        'limit': limit,
        'zone_area_id': zone_area_id,
        'QB': ''
    }
    headers['Referer'] = 'https://game.weixin.qq.com/cgi-bin/h5/static/smobadynamic/allbattle.html?openid=' + open_id + '&zone_area_id=' + str(zone_area_id) + '&ssid=1021&uin=&key=&pass_ticket=' + pass_ticket + '&abtest_cookie=BAABAAoACwASABMABAAjlx4AV5keAGmZHgBsmR4AAAA%3D&wx_header=1'
    r = requests.get(url, params=params, headers=headers, cookies=cookies, proxies=prox)
    temp = r.json()
    error_code = temp['errcode']
    logging.warn('load_user_game_list errorcode %s ip is %s openid %s' % (error_code, ip, open_id))
    if error_code == 40001:
        time.sleep(60 * 60 * 24)
    if error_code == 45009:
        # time.sleep(61)
        deprecate_big_ip(ip)
    if error_code != 0:
        raise Exception
    wfile = os.path.join(settings.Res_Battle_List_Dir, '%s_%s.txt' % (_profile(open_id), offset))
    with codecs.open(wfile, 'w', 'utf-8') as wf:
        wf.write(simplejson.dumps(temp, indent=2, sort_keys=True, ensure_ascii=False))
    duplicate.record_openid(open_id)
    has_next = temp['has_next']
    next_offset = temp['next_offset']
    return error_code, temp['battle_info']['battle_list'], open_id, has_next, next_offset


def load_game_detail(game_seq, game_svr_entity, relay_svr_entity, open_id, prox, ip):
    if duplicate.is_battle_has(game_seq):
        logging.warn('duplicate load_game_detail')
        return
    path = 'cgi-bin/gamewap/getsmobabattledetail'
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
    r = requests.get(url=url, params=params, headers=headers, cookies=cookies, proxies=prox)
    temp = r.json()
    error_code = temp['errcode']
    logging.warn('load_game_detail errorcode %s ip is %s' % (error_code, ip))
    if error_code == 40001:
        time.sleep(60 * 60 * 24)
    if error_code == 0:
        duplicate.record_game(game_seq)
    player_list = temp['normal_battle_detail']['user_battle_detail']
    if len(player_list) != 0:
        wfile = os.path.join(settings.Res_Battle_Detail_Dir, '%s.txt' % _battle_info(game_seq))
        with codecs.open(wfile, 'w', 'utf-8') as wf:
            wf.write(simplejson.dumps(temp, indent=2, sort_keys=True, ensure_ascii=False))
    profile_ids = []
    for player in player_list:
        profile_url = player['profile_url']
        profile_id = get_profileid_from_url(profile_url)
        profile_ids.append(profile_id)
    return error_code, profile_ids
