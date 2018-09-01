import requests

from config import redis

_ip_pool = '_ip_pool'
_deprecate_ip_pool = '_deprecate_ip_pool'
_key_ip_pool_url = 'ip_pool_url'

_ip_pool_url = 'http://dev.kdlapi.com/api/getproxy/'
orderid = redis.get('_ip_pool_orderid')
dedup = 1
_key_dedup = 'dedup'
pool_params = {
    'orderid': orderid,
    'num': 100,
    'b_pcchrome': 1,
    'b_pcie': 1,
    'b_pcff': 1,
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
    ip = str(redis.srandmember(_ip_pool, 1)[0], 'utf-8')
    proxies = {
        'http': 'http://%s' % ip
    }
    return proxies, ip


def fill_ip():
    current_ip_count = redis.scard(_ip_pool)
    if current_ip_count > 50:
        return
    url = redis.get(_key_ip_pool_url)
    response = requests.get(url, params=pool_params)
    temp = response.json()
    ip_list = temp['data']['proxy_list']
    for ip in ip_list:
        if redis.sismember(_deprecate_ip_pool, ip):
            continue
        redis.sadd(_ip_pool, ip)
    current_ip_count = redis.scard(_ip_pool)
    if current_ip_count < 50:
        pool_params[_key_dedup] = dedup
        fill_ip()
    else:
        if _key_dedup in pool_params:
            pool_params.pop(_key_dedup)


def deprecate_ip(ip):
    redis.srem(_ip_pool, ip)
    redis.sadd(_deprecate_ip_pool, ip)
    fill_ip()


# fill_ip()
# print('a' in pool_params.keys())
print(get_proxies())