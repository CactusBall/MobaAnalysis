from config import redis


def encode(value):
    if type(value) is bytes:
        return str(value, 'utf-8')
    return value


host = 'game.weixin.qq.com'
accept = '*/*'
accept_lang = 'zh-cn'
referer = 'https://game.weixin.qq.com/cgi-bin/h5/static/smobadynamic/index.html?game_svr_entity=2230&game_seq' \
          '=1535041351&relay_svr_entity=2618229376&openid=owanlsr79FJjp8n9KwkgaNwkthMA&zone_area_id=4050&ssid=1021' \
          '&abtest_cookie=AwABAAoACwATAAMAI5ceAFeZHgBjmR4AAAA%3D&pass_ticket=VpPOrckIvPf%2F6NP0INdWsn' \
          '%2FmcsdHHNkchFsCy2kOKpRYiVDvUODlOzsDKWLelhtX&wx_header=1'
accept_encoding = 'br, gzip, deflate'

ua = encode(redis.srandmember('wechat_game_uas', 1)[0])
key = encode(redis.get('wechat_game_key'))
pass_ticket = encode(redis.get('wechat_game_pass_ticket'))
uin = encode('MTEyNDEzMjI4MQ%3D%3D')
pgv_pvid = encode('971741250')
sd_cookie_crttime = encode('1530872150306')
sd_userid = encode('34911530872150306')

Res_UserInfo_Dir = '/Users/emrys/Documents/Moba/MobaUserInfo'
Res_Battle_List_Dir = '/Users/emrys/Documents/Moba/MobaBattleList'
Res_Battle_Detail_Dir = '/Users/emrys/Documents/Moba/MobaBattleDetail'
