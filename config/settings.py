from config import redis


def _encode(value):
    if type(value) is bytes:
        return str(value, 'utf-8')
    return value


host = 'game.weixin.qq.com'
accept = '*/*'
accept_lang = 'zh-cn'
referer = 'https://game.weixin.qq.com/cgi-bin/h5/static/profile_v1/index.html?t=g1NlbysGi4KDI5aTA0V-65f9QlaA&ssid=2902&abt=27'
accept_encoding = 'br, gzip, deflate'

ua = _encode(redis.srandmember('wechat_game_uas', 1)[0])
key = _encode(redis.get('wechat_game_key'))
pass_ticket = _encode(redis.get('wechat_game_pass_ticket'))
uin = _encode('MTEyNDEzMjI4MQ%3D%3D')
pgv_pvid = _encode('971741250')
sd_cookie_crttime = _encode('1530872150306')
sd_userid = _encode('34911530872150306')

Res_UserInfo_Dir = '/Users/emrys/Documents/Moba/MobaUserInfo'
Res_Battle_List_Dir = '/Users/emrys/Documents/Moba/MobaBattleList'
Res_Battle_Detail_Dir = '/Users/emrys/Documents/Moba/MobaBattleDetail'
