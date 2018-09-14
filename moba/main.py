import time

from config import redis
from config.settings import pass_ticket
from moba_tasks import get_user_info
from net.proxies import fill_ip

# fill_ip()
profile_id = 'g1NlbysGi4KDI5aTA0V-65f9QlaA'
# r = get_user_info.delay(profile_id)
# while not r.ready():
#     time.sleep(1)
# print(redis.scard('_ip_pool'))

# zone_area_id=32032
# print(
#     'https://game.weixin.qq.com/cgi-bin/h5/static/smobadynamic/allbattle.html?openid=' + profile_id + '&zone_area_id=' + str(zone_area_id) + '&ssid=1021&uin=&key=&pass_ticket=' + pass_ticket + '&abtest_cookie=BAABAAoACwASABMABAAjlx4AV5keAGmZHgBsmR4AAAA%3D&wx_header=1')
fill_ip()