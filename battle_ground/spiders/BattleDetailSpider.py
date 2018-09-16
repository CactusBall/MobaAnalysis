import logging
import os
import time

from configs import http, duplicate
from configs.duplicate import is_battle_has
from configs.settings import pass_ticket, key
from nets import get_openid_from_url, proxies
from spiders.CactusSpider import Spider


def _battle_info(game_id):
    return 'battle_%s' % game_id


def get_params(openid, team_id, battle_id, mode, dt_event_time):
    return {
        'openid': openid,
        'team_id': team_id,
        'plat_id': 0,
        'battle_id': battle_id,
        'mode': mode,
        'dt_event_time': dt_event_time,
        'type': '',
        'uin': '',
        'key': '',
        'pass_ticket': pass_ticket,
        'QB': ''
    }


def get_headers():
    return http.headers


def get_cookies():
    return {
        'pass_ticket': pass_ticket,
        'key': key,
        'uin': 'MTEyNDEzMjI4MQ%3D%3D',
        'qv_als': 'll1vj7NjTQFYEGF7A11537087975spj6uQ==',
        'pgv_pvid': '971741250',
        'pgv_pvi': '8852333568',
        'sd_cookie_crttime': '1530872150306',
        'sd_userid': '34911530872150306'
    }


class BattleDetailSpider(Spider):
    _data = ''
    _func = None

    def is_duplicate(self, params):
        return is_battle_has(params['battle_id'])

    def get_proxies(self):
        return proxies.get_proxies()[0]

    def get_file_path(self, params):
        file_dir = '/Users/emrys/Documents/BattleGround/BattleDetail'
        file_name = '%s.json' % _battle_info(params['battle_id'])
        return os.path.join(file_dir, file_name)

    def is_error(self, data):
        errorcode = data['errcode']
        if errorcode == 0:
            return 0, False
        else:
            return errorcode, True

    def do_error(self, code):
        if code == 40001:
            time.sleep(60 * 60 * 24)
        elif code == 45009:
            time.sleep(60)
        return True

    def request_end(self, params, data):
        duplicate.record_game(params['battle_id'])
        prey_list = data['prey_info']['prey_list']
        user_list = []
        for p in prey_list:
            if 'openid' in p:
                openid = p['openid']
            elif 'profile_url' in p:
                openid = get_openid_from_url(p['profile_url'])
            else:
                continue
            user_list.append(openid)
        return data['errcode'], user_list
