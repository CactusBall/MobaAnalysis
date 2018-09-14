import requests
import simplejson

from config import redis

_ip_pool = '_ip_pool'
_deprecate_ip_pool = '_deprecate_ip_pool'

_ip_pool_url = 'http://dev.kdlapi.com/api/getproxy/'
orderid = str(redis.get('_ip_pool_orderid'), 'utf-8')
dedup = 1
_key_dedup = 'dedup'
pool_params = {
    'orderid': orderid,
    'num': 1000,
    'b_pcchrome': 1,
    'b_pcie': 1,
    'b_pcff': 1,
    'b_android': 1,
    'b_iphone': 1,
    'protocol': 1,
    'method': 2,
    'an_an': 1,
    'an_ha': 1,
    'sp1': 1,
    'sp2': 1,
    'quality': 1,
    'sort': 1,
    'format': 'json',
    'sep': 1,
}


def get_proxies():
    ip_r = redis.srandmember(_ip_pool, 1)
    ip = str(ip_r[0], 'utf-8')
    proxies = {
        'http': 'http://%s' % ip
    }
    return proxies, ip


def get_big_proxies():
    ip_r = redis.srandmember('big_ip_pool', 1)
    ip = str(ip_r[0], 'utf-8')
    proxies = {
        'http': 'http://%s' % ip
    }
    return proxies, ip


def deprecate_big_ip(ip):
    redis.srem('big_ip_pool', ip)
    redis.sadd('big_ip_dep_pool', ip)


def fill_ip():
    # current_ip_count = redis.scard(_ip_pool)
    # if current_ip_count > 50:
    #     return
    url = _ip_pool_url
    url = 'http://svip.kdlapi.com/api/getproxy/?orderid=993693444425283&num=9999&b_pcchrome=1&b_pcie=1&b_pcff=1&b_iphone=1&protocol=2&method=2&an_an=1&an_ha=1&sp1=1&sp2=1&sp3=1&sort=1&format=json&sep=1'
    response = requests.get(url)
    temp = response.json()
    print(temp)
    ip_list = temp['data']['proxy_list']
    print('size %d' % len(ip_list))
    with open('/Users/emrys/Desktop/ip_1.json', 'w', encoding='utf-8') as f:
        f.write(simplejson.dumps(temp, indent=2, sort_keys=True, ensure_ascii=False))
    for ip in ip_list:
        # if redis.sismember(_deprecate_ip_pool, ip):
        #     continue
        redis.sadd('big_ip_pool', ip)
    current_ip_count = redis.scard('big_ip_pool')
    print(current_ip_count)
    # if current_ip_count < 50:
    #     pool_params[_key_dedup] = dedup
    # else:
    #     if _key_dedup in pool_params:
    #         pool_params.pop(_key_dedup)
