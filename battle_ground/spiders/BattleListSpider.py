import os
import time

from CactusSpider import Spider
from configs import http, duplicate
from configs.duplicate import is_user_has
from configs.settings import pass_ticket, key
from net import proxies


def _battle_list(openid):
    return 'list_%s' % openid


def get_params(openid, after_time):
    return {
        'openid': openid,
        'plat_id': 0,
        'limit': 20,
        'mode_type': 2,
        'after_time': after_time,
        'uin': '',
        'key': '',
        'pass_ticket': pass_ticket,
        'QB': '',
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


class BattleListSpider(Spider):

    def is_duplicate(self, params):
        return is_user_has(params['openid']) and params['after_time'] is 0

    def get_proxies(self):
        return proxies.get_proxies()[0]

    def get_file_path(self, params):
        file_dir = '/Users/emrys/Documents/BattleGround/BattleList'
        file_name = '%s_%s.json' % (_battle_list(params['openid']), params['after_time'])
        return os.path.join(file_dir, file_name)

    def is_error(self, data):
        errorcode = data['errcode']
        if errorcode is 0:
            return 0, False
        else:
            return errorcode, True

    def do_error(self, code):
        if code is 40001:
            time.sleep(60 * 60 * 24)
        elif code is 45009:
            time.sleep(60)
        return True

    def request_end(self, params, data):
        print('sadasfscmjanweqiflen')
        duplicate.record_user(params['openid'])
        return data['errcode'], data['has_next'], data['next_after_time'], data['battle_list']
